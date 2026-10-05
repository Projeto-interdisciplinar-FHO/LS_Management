from django.db import transaction

from apps.health.vaccinations.models import Vaccination
from apps.herd.animals.models import Animal
from apps.herd.quadrants.models import Quadrant
from apps.health.vaccines.models import Vaccine


class VaccinationFacade:
    """Orquestra a aplicação de vacina para todos os animais de um quadrante."""

    @staticmethod
    @transaction.atomic
    def apply_batch(
        quadrant_id,
        vaccine_id,
        vaccination_date,
        next_vaccination_date,
        dosage,
    ):
        quadrant = Quadrant.objects.get(id=quadrant_id)
        vaccine = Vaccine.objects.get(id=vaccine_id)
        animals = Animal.objects.filter(
            quadrant_id=quadrant_id,
            status="ativo",
        )

        if not animals.exists():
            raise ValueError(
                f"Nenhum animal ativo encontrado no quadrante {quadrant.name}"
            )

        vaccinated_animals = []
        for animal in animals:
            Vaccination.objects.create(
                animal=animal,
                vaccine=vaccine,
                dosage=dosage,
                vaccination_date=vaccination_date,
                next_vaccination_date=next_vaccination_date,
                vaccination_status=True,
            )
            vaccinated_animals.append({
                "id": animal.id,
                "name": animal.name,
                "register_number": animal.register_number,
            })

        vaccinated_count = len(vaccinated_animals)
        return {
            "success": True,
            "vaccinated_count": vaccinated_count,
            "animals": vaccinated_animals,
            "message": (
                f"{vaccinated_count} animais vacinados com sucesso "
                f"no quadrante {quadrant.name}!"
            ),
        }