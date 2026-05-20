import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from animals.models import Animal
from vaccines.models import Vaccine
from vaccinations.models import Vaccination
from datetime import date, timedelta

# Criar vacina de teste
vaccine, created = Vaccine.objects.get_or_create(name='Brucelose')
print(f"Vacina: {vaccine.name} (ID: {vaccine.id})")

# Pegar um animal de teste
try:
    animal = Animal.objects.first()
    if animal:
        print(f"Animal: {animal.name} (ID: {animal.id})")
        
        # Criar vacinação
        vacc = Vaccination.objects.create(
            animal=animal,
            vaccine=vaccine,
            vaccination_date=date.today() - timedelta(days=30),
            next_vaccination_date=date.today() + timedelta(days=5),
            dosage=5.0,
            doses_taken=1,
            vaccination_status=True  # Boolean: True = Aplicada
        )
        print(f"Vacinação criada: {vacc.id}")
        print(f"Data: {vacc.vaccination_date}")
        print(f"Próxima dose: {vacc.next_vaccination_date}")
        print(f"Status: {vacc.vaccination_status}")
        print(f"É atrasada: {vacc.is_overdue}")
        print(f"Dias até próxima: {vacc.days_until_next}")
    else:
        print("Nenhum animal encontrado")
except Exception as e:
    print(f"Erro: {e}")
