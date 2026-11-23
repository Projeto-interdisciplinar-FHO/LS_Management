from rest_framework import generics
from apps.herd.animals.models import Animal
from apps.herd.animals.serializers import AnimalSerializer

class AnimalListView(generics.ListCreateAPIView):
    """Listagem e criação de animais"""
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer

class AnimalRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
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

        return super().destroy(request, *args, **kwargs)