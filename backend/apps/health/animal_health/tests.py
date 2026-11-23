from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from apps.health.animal_health.models import AnimalHealth
from apps.herd.breeds.models import Breed
from apps.herd.cattle.models import Cow


class AnimalHealthApiTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(username="animal-health-test")
        self.client = APIClient()
        self.client.force_authenticate(user)

        breed = Breed.objects.create(name="Teste")
        self.first_animal = Cow.objects.create(
            name="Matriz A",
            breed=breed,
            register_number=910001,
        )
        second_animal = Cow.objects.create(
            name="Matriz B",
            breed=breed,
            register_number=910002,
        )
        self.record = AnimalHealth.objects.create(
            animal=self.first_animal,
            consultation_date=date(2026, 1, 1),
            consultation_reason="Consulta de teste",
        )
        AnimalHealth.objects.create(
            animal=second_animal,
            consultation_date=date(2026, 1, 2),
            consultation_reason="Consulta de teste",
        )

    def test_animal_filter_returns_only_that_animals_records(self):
        response = self.client.get(
            "/animal_health/",
            {"animal_id": self.first_animal.id},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual([item["id"] for item in response.data], [self.record.id])

    def test_delete_detail_route_removes_the_selected_record(self):
        response = self.client.delete(f"/animal_health/{self.record.id}/")

        self.assertEqual(response.status_code, 204)
        self.assertFalse(AnimalHealth.objects.filter(pk=self.record.id).exists())
