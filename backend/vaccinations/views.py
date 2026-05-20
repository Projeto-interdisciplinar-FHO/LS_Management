from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from vaccinations.models import Vaccination
from vaccinations.serializers import VaccinationSerializer

class VaccinationCreateListView(generics.ListCreateAPIView):
    queryset = Vaccination.objects.all()
    serializer_class = VaccinationSerializer

class VaccinationRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vaccination.objects.all()
    serializer_class = VaccinationSerializer

@api_view(['GET'])
def vaccinations_by_animal(request, animal_id):
    """Retorna todas as vacinações de um animal específico"""
    try:
        vaccinations = Vaccination.objects.filter(animal_id=animal_id).select_related('vaccine', 'animal')
        serializer = VaccinationSerializer(vaccinations, many=True)
        # Enriquecer dados com informações do animal e vacina
        data = []
        for vacc in vaccinations:
            vacc_data = {
                'id': vacc.id,
                'animal_id': vacc.animal.id,
                'animal_name': vacc.animal.name,
                'vaccine_id': vacc.vaccine.id,
                'vaccine_name': vacc.vaccine.name,
                'vaccination_date': vacc.vaccination_date,
                'next_vaccination_date': vacc.next_vaccination_date,
                'dosage': vacc.dosage,
                'doses_taken': vacc.doses_taken,
                'total_doses': vacc.total_doses,
                'vaccination_status': vacc.vaccination_status,
                'periodicity': vacc.periodicity
            }
            data.append(vacc_data)
        return Response(data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def upcoming_vaccinations(request):
    """Retorna vacinações próximas (próximos 7 dias)"""
    try:
        today = timezone.now().date()
        seven_days = today + timedelta(days=7)
        
        vaccinations = Vaccination.objects.filter(
            next_vaccination_date__gte=today,
            next_vaccination_date__lte=seven_days
        ).select_related('vaccine', 'animal').order_by('next_vaccination_date')
        
        data = []
        for vacc in vaccinations:
            vacc_data = {
                'id': vacc.id,
                'animal_id': vacc.animal.id,
                'animal_name': vacc.animal.name,
                'vaccine_id': vacc.vaccine.id,
                'vaccine_name': vacc.vaccine.name,
                'vaccination_date': vacc.vaccination_date,
                'next_vaccination_date': vacc.next_vaccination_date,
                'dosage': vacc.dosage,
                'vaccination_status': vacc.vaccination_status
            }
            data.append(vacc_data)
        return Response(data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)