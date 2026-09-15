from django.contrib import admin
from apps.herd.animals.models import Animal

class AnimalAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'register_number', 'birth_date', 'sex', 'active',)
    search_fields = ('id', 'name',)

admin.site.register(Animal, AnimalAdmin)