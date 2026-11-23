from datetime import date
from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from apps.herd.breeds.models import Breed
from apps.herd.cattle.models import Bull, Cow
from apps.reproduction.models import (
    Birth,
    BirthOccurrence,
    DryOff,
    EmbryoTransfer,
    Insemination,
    PregnancyDiagnosis,
    ReproductiveAnalysis,
)


class ReproductiveWorkflowTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="reproduction-test")
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.breed = Breed.objects.create(name="Teste")
        occurrence = BirthOccurrence.objects.create(description="Parto simples")
        birth = Birth.objects.create(
            occurrence=occurrence,
            date=date(2020, 1, 1),
            weight=Decimal("35.00"),
        )
        self.cow = Cow.objects.create(
            name="Matriz teste",
            breed=self.breed,
            register_number=900001,
            birth=birth,
        )
        self.donor = Cow.objects.create(
            name="Doadora teste",
            breed=self.breed,
            register_number=900002,
            birth=birth,
        )
        self.bull = Bull.objects.create(
            name="Touro teste",
            breed=self.breed,
            register_number=900003,
        )
        self.procedure_date = timezone.localdate()

    @patch("integrations.gemini_api.views.validar_reproducao")
    def test_analysis_is_saved_and_returns_id(self, analyze):
        analyze.return_value = {
            "apto": True,
            "status": "APROVADO",
            "veredito_final": "Cruzamento apto.",
        }

        response = self.client.post(
            "/api/reproducao/validar-genealogia/",
            {
                "cow_id": self.cow.id,
                "bull_id": self.bull.id,
                "date": self.procedure_date.isoformat(),
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["apto"])
        self.assertEqual(response.data["analysis_id"], ReproductiveAnalysis.objects.get().id)
        self.assertEqual(ReproductiveAnalysis.objects.get().requested_by, self.user)
        analyze.assert_called_once()

    @patch("integrations.gemini_api.views.validar_reproducao")
    def test_analysis_id_can_register_matching_insemination(self, analyze):
        analyze.return_value = {
            "apto": True,
            "status": "APROVADO",
            "veredito_final": "Cruzamento apto.",
        }
        analysis_response = self.client.post(
            "/api/reproducao/validar-genealogia/",
            {
                "cow_id": self.cow.id,
                "bull_id": self.bull.id,
                "date": self.procedure_date.isoformat(),
            },
            format="json",
        )

        response = self.client.post(
            "/inseminations/",
            {
                "mother": self.cow.id,
                "father": self.bull.id,
                "date": self.procedure_date.isoformat(),
                "analysis_id": analysis_response.data["analysis_id"],
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Insemination.objects.get().analysis_id, analysis_response.data["analysis_id"])

    def test_analysis_route_requires_authentication(self):
        response = APIClient().post(
            "/api/reproducao/validar-genealogia/",
            {"cow_id": self.cow.id, "bull_id": self.bull.id},
            format="json",
        )
        self.assertEqual(response.status_code, 401)

    @patch("integrations.gemini_api.views.validar_reproducao")
    def test_underage_cow_is_hard_blocked_without_calling_ai(self, analyze):
        occurrence = BirthOccurrence.objects.get(description="Parto simples")
        birth = Birth.objects.create(
            occurrence=occurrence,
            date=self.procedure_date.replace(year=self.procedure_date.year - 1),
            weight=Decimal("35.00"),
        )
        young_cow = Cow.objects.create(
            name="Matriz jovem",
            breed=self.breed,
            register_number=900004,
            birth=birth,
        )

        response = self.client.post(
            "/api/reproducao/validar-genealogia/",
            {
                "cow_id": young_cow.id,
                "bull_id": self.bull.id,
                "date": self.procedure_date.isoformat(),
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data["apto"])
        self.assertTrue(response.data["hard_block"])
        analyze.assert_not_called()

    def test_insemination_requires_analysis_confirmation_and_reason_for_override(self):
        analysis = ReproductiveAnalysis.objects.create(
            cow=self.cow,
            bull=self.bull,
            result={"apto": False, "hard_block": False, "status": "ERRO_CONFIGURACAO"},
            requested_by=self.user,
        )
        payload = {
            "mother": self.cow.id,
            "father": self.bull.id,
            "date": self.procedure_date.isoformat(),
            "analysis_id": analysis.id,
        }

        response = self.client.post("/inseminations/", payload, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Insemination.objects.exists())

        payload["manual_override_reason"] = "Revisão clínica autorizada."
        response = self.client.post("/inseminations/", payload, format="json")
        self.assertEqual(response.status_code, 400)
        payload["manual_override_confirmed"] = True
        response = self.client.post("/inseminations/", payload, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data["manual_override_confirmed"])
        self.assertEqual(response.data["manual_override_reason"], payload["manual_override_reason"])
        self.assertEqual(Insemination.objects.get().analysis, analysis)

    def test_insemination_cannot_override_hard_block(self):
        analysis = ReproductiveAnalysis.objects.create(
            cow=self.cow,
            bull=self.bull,
            result={
                "apto": False,
                "hard_block": True,
                "bloqueio_motivo": "Matriz abaixo da idade mínima.",
            },
        )
        response = self.client.post(
            "/inseminations/",
            {
                "mother": self.cow.id,
                "father": self.bull.id,
                "date": self.procedure_date.isoformat(),
                "analysis_id": analysis.id,
                "manual_override_confirmed": True,
                "manual_override_reason": "Revisão clínica autorizada.",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Insemination.objects.exists())

    def test_diagnosis_and_dry_off_require_positive_pregnancy(self):
        insemination = Insemination.objects.create(
            mother=self.cow,
            father=self.bull,
            date=self.procedure_date,
        )
        diagnosis_response = self.client.post(
            "/pregnancy-diagnoses/",
            {
                "insemination": insemination.id,
                "method": "ultrasound",
                "result": "positive",
                "date": self.procedure_date.isoformat(),
                "notes": "",
            },
            format="json",
        )
        self.assertEqual(diagnosis_response.status_code, 201)
        diagnosis_id = diagnosis_response.data["id"]

        DryOff.objects.create(
            pregnancy_diagnosis=PregnancyDiagnosis.objects.get(pk=diagnosis_id),
            date=self.procedure_date,
        )
        duplicate_response = self.client.post(
            "/dry-offs/",
            {
                "pregnancy_diagnosis": diagnosis_id,
                "date": self.procedure_date.isoformat(),
                "notes": "",
            },
            format="json",
        )
        self.assertEqual(duplicate_response.status_code, 400)

    def test_embryo_transfer_uses_analysis_for_donor_and_bull(self):
        analysis = ReproductiveAnalysis.objects.create(
            cow=self.donor,
            bull=self.bull,
            result={"apto": False, "hard_block": False, "status": "REVISAR"},
        )
        payload = {
            "recipient": self.cow.id,
            "donor": self.donor.id,
            "father": self.bull.id,
            "date": self.procedure_date.isoformat(),
            "embryo_reference": "EMB-TEST",
            "analysis_id": analysis.id,
            "manual_override_reason": "Revisão clínica autorizada.",
        }
        response = self.client.post(
            "/embryo-transfers/",
            payload,
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        payload["manual_override_confirmed"] = True
        response = self.client.post("/embryo-transfers/", payload, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data["manual_override_confirmed"])
        self.assertEqual(EmbryoTransfer.objects.get().analysis, analysis)
