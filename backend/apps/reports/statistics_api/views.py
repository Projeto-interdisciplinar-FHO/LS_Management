from rest_framework import views, response, status
from django.db.models import Sum
from django.db.models.functions import TruncMonth

from apps.herd.animals.models import Animal
from apps.herd.species.models import Specie
from apps.herd.breeds.models import Breed
from apps.herd.quadrants.models import Quadrant
from apps.production.milk_production_history.models import MilkProductionHistory
from apps.health.vaccinations.models import Vaccination

def get_milk_stats():
    stats_query = (
        MilkProductionHistory.objects
        .annotate(month=TruncMonth('production_date'))
        .values('month')
        .annotate(total=Sum('milk_production'))
        .order_by('month')
    )
    
    return [
        {
            'month': stat['month'].strftime('%Y-%m'),
            'total': float(stat['total'])
        } 
        for stat in stats_query
    ]

class ApiStatsView(views.APIView):

    def get(self, request):
        total_animals = Animal.objects.count()
        total_species = Specie.objects.count()
        total_breeds = Breed.objects.count()
        total_quadrants = Quadrant.objects.count()
        total_vaccinations = Vaccination.objects.count()

        return response.Response(data={
            'total_animals': total_animals,
            'total_species': total_species,
            'total_breeds': total_breeds,
            'total_quadrants': total_quadrants,
            'total_vaccinations': total_vaccinations,
            'total_milk_production': get_milk_stats(),
        }, status=status.HTTP_200_OK)