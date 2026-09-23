from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from apps.health.vaccinations.models import Vaccination
from apps.health.vaccinations.serializers import VaccinationSerializer
from apps.health.vaccinations.facades import VaccinationFacade
from apps.herd.quadrants.models import Quadrant
from apps.health.vaccines.models import Vaccine

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


@api_view(['POST'])
def batch_vaccination(request):
    """
    Aplicar vacinação em lote a todos os animais de um quadrante.
    
    POST /vaccinations/batch/
    {
        "quadrant_id": 1,
        "vaccine_id": 5,
        "vaccination_date": "2026-05-24",
        "next_vaccination_date": "2026-06-24",
        "dosage": 5.00
    }
    
    Retorna: {
        "success": true,
        "vaccinated_count": 6,
        "animals": [
            {"id": 1, "name": "Mimosa", "register_number": 142},
            ...
        ],
        "message": "6 animais vacinados com sucesso!"
    }
    """
    try:
        quadrant_id = request.data.get('quadrant_id')
        vaccine_id = request.data.get('vaccine_id')
        vaccination_date = request.data.get('vaccination_date')
        next_vaccination_date = request.data.get('next_vaccination_date')
        dosage = request.data.get('dosage')
        
        # Validações básicas
        if not all([quadrant_id, vaccine_id, vaccination_date, dosage]):
            return Response(
                {'error': 'Parâmetros obrigatórios: quadrant_id, vaccine_id, vaccination_date, dosage'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        result = VaccinationFacade.apply_batch(
            quadrant_id=quadrant_id,
            vaccine_id=vaccine_id,
            vaccination_date=vaccination_date,
            next_vaccination_date=next_vaccination_date,
            dosage=dosage,
        )
        return Response(result, status=status.HTTP_201_CREATED)
        
    except (Quadrant.DoesNotExist, Vaccine.DoesNotExist):
        return Response(
            {'error': 'Quadrante ou vacina não encontrada'},
            status=status.HTTP_404_NOT_FOUND
        )
    except ValueError as error:
        return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(
            {'error': f'Erro ao processar vacinação em lote: {str(e)}'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
def quadrant_animals_count(request, quadrant_id):
    """
    Retorna o número de animais ativos em um quadrante.
    Útil para mostrar dinamicamente quantos serão vacinados.
    
    GET /vaccinations/quadrant/{quadrant_id}/animals-count/
    
    Retorna: {
        "quadrant_id": 1,
        "quadrant_name": "Piquete 1",
        "active_animals_count": 6,
        "animals": [
            {"id": 1, "name": "Mimosa", "register_number": 142},
            ...
        ]
    }
    """
    from apps.herd.animals.models import Animal
    from apps.herd.quadrants.models import Quadrant
    
    try:
        quadrant = Quadrant.objects.get(id=quadrant_id)
        animals = Animal.objects.filter(
            quadrant_id=quadrant_id,
            status='ativo'
        ).values('id', 'name', 'register_number')
        
        return Response({
            'quadrant_id': quadrant.id,
            'quadrant_name': quadrant.name,
            'active_animals_count': len(animals),
            'animals': list(animals)
        })
    except Quadrant.DoesNotExist:
        return Response(
            {'error': 'Quadrante não encontrado'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )