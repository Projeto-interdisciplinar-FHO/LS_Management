import csv

from django.db.models import OuterRef, Prefetch, Subquery
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.health.animal_health.models import AnimalHealth
from apps.health.vaccinations.models import Vaccination
from apps.movements.animal_movements.models import AnimalMovement
from apps.production.milk_production_history.models import Milking
from apps.production.weight_history.models import WeightHistory

from .models import Cow


ANIMAL_EXPORT_FIELDS = {
    "id": "ID",
    "name": "Nome",
    "register_number": "Número de registro",
    "status": "Status",
    "score": "Escore",
    "reproductive_status": "Status reprodutivo",
    "breed_id": "ID da raça",
    "breed_name": "Raça",
    "birth_id": "ID do nascimento",
    "birth_date": "Data de nascimento",
    "birth_weight": "Peso ao nascer",
    "birth_type": "Tipo de nascimento",
    "current_quadrant_id": "ID do estábulo",
    "current_quadrant_name": "Estábulo",
    "last_movement_date": "Data da última movimentação",
    "last_weight": "Último peso",
    "last_weighing_date": "Data da última pesagem",
    "total_weight_records": "Quantidade de pesagens",
    "total_vaccinations": "Quantidade de vacinações",
    "last_vaccination_date": "Data da última vacinação",
    "total_milk_production": "Produção de leite acumulada",
    "total_milkings": "Quantidade de ordenhas",
    "last_milking_date": "Data da última ordenha",
    "total_feedings": "Quantidade de alimentações",
    "total_health_records": "Quantidade de registros médicos",
    "total_inseminations": "Quantidade de inseminações",
}


class AnimalExportMixin:
    @staticmethod
    def _export_queryset():
        latest_movement = AnimalMovement.objects.filter(
            animal=OuterRef("pk")
        ).order_by("-movement_date", "-pk")

        return Cow.objects.select_related(
            "breed", "birth__occurrence"
        ).prefetch_related(
            Prefetch(
                "movements",
                queryset=AnimalMovement.objects.select_related("quadrant").order_by(
                    "-movement_date", "-pk"
                ),
                to_attr="export_movements",
            ),
            Prefetch(
                "weight_history",
                queryset=WeightHistory.objects.order_by("-weighing_date", "-pk"),
                to_attr="export_weights",
            ),
            Prefetch(
                "vaccine_applications",
                queryset=Vaccination.objects.order_by("-vaccination_date", "-pk"),
                to_attr="export_vaccinations",
            ),
            Prefetch(
                "milkings",
                queryset=Milking.objects.order_by("-production_date", "-pk"),
                to_attr="export_milkings",
            ),
            Prefetch("feedings", to_attr="export_feedings"),
            Prefetch(
                "health_records",
                queryset=AnimalHealth.objects.all(),
                to_attr="export_health_records",
            ),
            Prefetch("inseminations", to_attr="export_inseminations"),
        ).annotate(
            export_quadrant_id=Subquery(
                latest_movement.values("quadrant_id")[:1]
            )
        )

    @staticmethod
    def _export_value(animal, field):
        movements = getattr(animal, "export_movements", [])
        weights = getattr(animal, "export_weights", [])
        vaccinations = getattr(animal, "export_vaccinations", [])
        milkings = getattr(animal, "export_milkings", [])
        latest_movement = movements[0] if movements else None
        latest_weight = weights[0] if weights else None
        latest_vaccination = vaccinations[0] if vaccinations else None
        latest_milking = milkings[0] if milkings else None
        birth = animal.birth

        values = {
            "id": animal.id,
            "name": animal.name,
            "register_number": animal.register_number,
            "status": animal.status,
            "score": animal.score,
            "reproductive_status": animal.reproductive_status,
            "breed_id": animal.breed_id,
            "breed_name": animal.breed.name,
            "birth_id": animal.birth_id,
            "birth_date": birth.date if birth else None,
            "birth_weight": birth.weight if birth else None,
            "birth_type": birth.occurrence.description if birth else None,
            "current_quadrant_id": latest_movement.quadrant_id if latest_movement else None,
            "current_quadrant_name": (
                latest_movement.quadrant.name if latest_movement else None
            ),
            "last_movement_date": (
                latest_movement.movement_date if latest_movement else None
            ),
            "last_weight": latest_weight.weight if latest_weight else None,
            "last_weighing_date": (
                latest_weight.weighing_date if latest_weight else None
            ),
            "total_weight_records": len(weights),
            "total_vaccinations": len(vaccinations),
            "last_vaccination_date": (
                latest_vaccination.vaccination_date if latest_vaccination else None
            ),
            "total_milk_production": sum(
                (milking.milk_production for milking in milkings), 0
            ),
            "total_milkings": len(milkings),
            "last_milking_date": (
                latest_milking.production_date if latest_milking else None
            ),
            "total_feedings": len(getattr(animal, "export_feedings", [])),
            "total_health_records": len(getattr(animal, "export_health_records", [])),
            "total_inseminations": len(getattr(animal, "export_inseminations", [])),
        }
        return values[field]

    @action(detail=False, methods=["get"], url_path="export-fields")
    def export_fields(self, request):
        return Response(
            [
                {"key": key, "label": label}
                for key, label in ANIMAL_EXPORT_FIELDS.items()
            ]
        )

    @action(detail=False, methods=["get"], url_path="export")
    def export(self, request):
        requested_fields = request.query_params.get("fields")
        fields = (
            [field.strip() for field in requested_fields.split(",") if field.strip()]
            if requested_fields
            else list(ANIMAL_EXPORT_FIELDS)
        )

        invalid_fields = sorted(set(fields) - set(ANIMAL_EXPORT_FIELDS))
        if invalid_fields:
            return Response(
                {
                    "detail": "Um ou mais campos de exportação são inválidos.",
                    "invalid_fields": invalid_fields,
                    "available_fields": list(ANIMAL_EXPORT_FIELDS),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not fields:
            return Response(
                {"detail": "Informe ao menos um campo em fields."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        quadrant_id = request.query_params.get(
            "quadrant_id", request.query_params.get("estabulo_id")
        )
        queryset = self._export_queryset()
        if quadrant_id and quadrant_id.lower() != "all":
            try:
                quadrant_id = int(quadrant_id)
            except ValueError:
                return Response(
                    {"detail": "quadrant_id deve ser um número inteiro ou 'all'."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            queryset = queryset.filter(export_quadrant_id=quadrant_id)

        response = HttpResponse(content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = 'attachment; filename="animais.csv"'
        response.write("\ufeff")
        writer = csv.writer(response)
        writer.writerow([ANIMAL_EXPORT_FIELDS[field] for field in fields])
        for animal in queryset:
            writer.writerow([self._export_value(animal, field) for field in fields])
        return response
