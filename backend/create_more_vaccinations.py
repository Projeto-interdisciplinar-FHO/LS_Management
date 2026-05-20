import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from animals.models import Animal
from vaccines.models import Vaccine
from vaccinations.models import Vaccination
from datetime import date, timedelta

# Criar vacinas de teste
vaccines = {
    'Brucelose': Vaccine.objects.get_or_create(name='Brucelose')[0],
    'Leptospirose': Vaccine.objects.get_or_create(name='Leptospirose')[0],
    'Raiva': Vaccine.objects.get_or_create(name='Raiva')[0],
    'IBR': Vaccine.objects.get_or_create(name='IBR')[0],
}

# Pegar 3 animais
animals = Animal.objects.all()[:3]

if len(animals) >= 2:
    # Animal 1 - Brucelose ATRASADA (5 dias atrás)
    Vaccination.objects.create(
        animal=animals[0],
        vaccine=vaccines['Brucelose'],
        vaccination_date=date.today() - timedelta(days=60),
        next_vaccination_date=date.today() - timedelta(days=5),
        dosage=5.0,
        doses_taken=1,
        vaccination_status=True
    )
    print(f"✓ Criada: {animals[0].name} - Brucelose ATRASADA (5 dias)")
    
    # Animal 1 - Leptospirose PRÓXIMOS 3 DIAS
    Vaccination.objects.create(
        animal=animals[0],
        vaccine=vaccines['Leptospirose'],
        vaccination_date=date.today() - timedelta(days=60),
        next_vaccination_date=date.today() + timedelta(days=3),
        dosage=5.0,
        doses_taken=1,
        vaccination_status=True
    )
    print(f"✓ Criada: {animals[0].name} - Leptospirose PRÓXIMOS 3 DIAS")
    
    # Animal 2 - Raiva EM DIA (próxima em 20 dias)
    Vaccination.objects.create(
        animal=animals[1],
        vaccine=vaccines['Raiva'],
        vaccination_date=date.today() - timedelta(days=30),
        next_vaccination_date=date.today() + timedelta(days=20),
        dosage=2.0,
        doses_taken=1,
        vaccination_status=True
    )
    print(f"✓ Criada: {animals[1].name} - Raiva EM DIA")
    
    # Animal 2 - IBR ATRASADA (20 dias atrás)
    Vaccination.objects.create(
        animal=animals[1],
        vaccine=vaccines['IBR'],
        vaccination_date=date.today() - timedelta(days=30),
        next_vaccination_date=date.today() - timedelta(days=20),
        dosage=3.0,
        doses_taken=1,
        vaccination_status=True
    )
    print(f"✓ Criada: {animals[1].name} - IBR ATRASADA (20 dias)")
    
    if len(animals) >= 3:
        # Animal 3 - Brucelose PRÓXIMOS 6 DIAS
        Vaccination.objects.create(
            animal=animals[2],
            vaccine=vaccines['Brucelose'],
            vaccination_date=date.today() - timedelta(days=60),
            next_vaccination_date=date.today() + timedelta(days=6),
            dosage=5.0,
            doses_taken=1,
            vaccination_status=True
        )
        print(f"✓ Criada: {animals[2].name} - Brucelose PRÓXIMOS 6 DIAS")
        
        # Animal 3 - Leptospirose EM DIA (próxima em 15 dias)
        Vaccination.objects.create(
            animal=animals[2],
            vaccine=vaccines['Leptospirose'],
            vaccination_date=date.today() - timedelta(days=30),
            next_vaccination_date=date.today() + timedelta(days=15),
            dosage=5.0,
            doses_taken=1,
            vaccination_status=True
        )
        print(f"✓ Criada: {animals[2].name} - Leptospirose EM DIA")

print("\nResumo:")
print("Atrasadas: 2 (Brucelose e IBR)")
print("Próximos 7 dias: 2 (Leptospirose e Brucelose)")
print("Em Dia: 2 (Raiva e Leptospirose)")
print("Total criadas: 6 vacinações de teste")
