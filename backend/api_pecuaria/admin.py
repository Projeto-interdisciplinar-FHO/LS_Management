from django.contrib import admin

from django.contrib import admin
from animals.models import Animal
from animal_health.models import AnimalHealth
from vaccinations.models import Vaccination
from vaccines.models import Vaccine
from weight_history.models import WeightHistory
from species.models import Specie
from purpose_types.models import PurposeType
 
 
admin.site.register(Animal)
admin.site.register(AnimalHealth)
admin.site.register(Vaccination)
admin.site.register(Vaccine)
admin.site.register(WeightHistory)
admin.site.register(Specie)
admin.site.register(PurposeType)
 