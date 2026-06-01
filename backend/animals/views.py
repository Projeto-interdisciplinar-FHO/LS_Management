from django.db import connection
from rest_framework import generics
from animals.models import Animal
from animals.serializers import AnimalSerializer
from rest_framework.permissions import AllowAny

class AnimalListView(generics.ListCreateAPIView):
    """Listagem e criação de animais"""
    permission_classes = (AllowAny,)
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer

class AnimalRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (AllowAny,)
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Limpa os registros dependentes antes de apagar o animal para evitar problemas de integridade na base SQLite.
        instance.health_records.all().delete()
        instance.movements.all().delete()
        instance.feeding_plans.all().delete()
        instance.feedings.all().delete()
        instance.vaccination_plans.all().delete()
        instance.weight_history.all().delete()
        instance.milk_production_history.all().delete()
        instance.vaccination_set.all().delete()
        instance.notifications.all().update(animal=None)
        instance.tasks.all().update(animal=None)

        # Limpa tabelas antigas que ainda existem no banco e possuem FK para o animal.
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM animal_biometrics_animalalert WHERE animal_id = %s",
                [instance.id],
            )
            cursor.execute(
                "DELETE FROM animal_biometrics_biometricreading WHERE animal_id = %s",
                [instance.id],
            )

        return super().destroy(request, *args, **kwargs)