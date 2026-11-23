from datetime import date
from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from openpyxl import Workbook
from rest_framework.test import APIClient

from apps.herd.breeds.models import Breed
from apps.herd.cattle.models import Cow
from apps.production.milk_production_history.models import Milking


def planilha(cabecalhos, *linhas):
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(cabecalhos)
    for linha in linhas:
        sheet.append(linha)
    output = BytesIO()
    workbook.save(output)
    return output.getvalue()


class ImportacaoTransacionalTests(TestCase):
    def setUp(self):
        admin = get_user_model().objects.create_superuser(
            username="import-test",
            email="import@example.test",
            password="test-password",
        )
        self.client = APIClient()
        self.client.force_authenticate(admin)
        self.breed = Breed.objects.create(name="Holandesa")
        self.cow = Cow.objects.create(
            name="Vaca existente",
            breed=self.breed,
            register_number=910001,
        )

    def arquivo(self, nome, cabecalhos, *linhas):
        return SimpleUploadedFile(
            nome,
            planilha(cabecalhos, *linhas),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    def test_vaca_import_preview_does_not_save_and_confirmation_saves(self):
        upload = self.arquivo(
            "vacas.xlsx",
            ["Número do Brinco", "Nome do Bovino", "Raça"],
            [910002, "Vaca importada", "Holandesa"],
        )
        preview = self.client.post(
            "/importacao/vacas/?dry_run=true",
            {"file": upload},
            format="multipart",
        )
        self.assertEqual(preview.status_code, 200)
        self.assertTrue(preview.data["dry_run"])
        self.assertEqual(preview.data["total_importados"], 1)
        self.assertFalse(Cow.objects.filter(register_number=910002).exists())

        upload = self.arquivo(
            "vacas.xlsx",
            ["Número do Brinco", "Nome do Bovino", "Raça"],
            [910002, "Vaca importada", "Holandesa"],
        )
        saved = self.client.post(
            "/importacao/vacas/?abortar_se_houver_erros=true",
            {"file": upload},
            format="multipart",
        )
        self.assertEqual(saved.status_code, 201)
        self.assertEqual(saved.data["total_importados"], 1)
        self.assertTrue(Cow.objects.filter(register_number=910002).exists())

    def test_milking_import_preview_does_not_save_and_confirmation_saves(self):
        values = ["Número do Brinco", "Produção (Litros)", "Data da Ordenha"]
        row = [self.cow.register_number, 12.5, date(2026, 11, 20)]
        preview = self.client.post(
            "/importacao/ordenhas/?dry_run=true",
            {"file": self.arquivo("ordenhas.xlsx", values, row)},
            format="multipart",
        )
        self.assertEqual(preview.status_code, 200)
        self.assertTrue(preview.data["dry_run"])
        self.assertEqual(preview.data["total_importados"], 1)
        self.assertFalse(Milking.objects.exists())

        saved = self.client.post(
            "/importacao/ordenhas/",
            {"file": self.arquivo("ordenhas.xlsx", values, row)},
            format="multipart",
        )
        self.assertEqual(saved.status_code, 201)
        self.assertEqual(saved.data["total_importados"], 1)
        self.assertTrue(Milking.objects.filter(animal=self.cow).exists())

    def test_milking_confirmation_aborts_when_any_row_is_invalid(self):
        response = self.client.post(
            "/importacao/ordenhas/?abortar_se_houver_erros=true",
            {
                "file": self.arquivo(
                    "ordenhas.xlsx",
                    ["Número do Brinco", "Produção (Litros)", "Data da Ordenha"],
                    [self.cow.register_number, 12.5, date(2026, 11, 20)],
                    [919999, 10.0, date(2026, 11, 20)],
                )
            },
            format="multipart",
        )
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Milking.objects.exists())
