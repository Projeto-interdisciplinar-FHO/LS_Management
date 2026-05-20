from django.shortcuts import render
from rest_framework import views, response, status
from django.db.models import Sum
from django.db.models.functions import TruncMonth

from animals.models import Animal
from species.models import Specie
from breeds.models import Breed
from quadrants.models import Quadrant
from milk_production_history.models import MilkProductionHistory
from vaccinations.models import Vaccination

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