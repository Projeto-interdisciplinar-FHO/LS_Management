"""
Script para popular a base de dados com dados de teste de biometria.
Execute com: python manage.py shell < seed_biometrics.py
"""

import random
from datetime import datetime, timedelta
from django.utils import timezone

from animals.models import Animal
from animal_biometrics.models import BiometricReading, AnimalAlert

def create_biometric_data():
    """
    Cria dados de biometria realistas para os primeiros 5 animais.
    Simula leituras dos últimos 7 dias.
    """
    animals = Animal.objects.all()[:5]
    
    if not animals:
        print("❌ Nenhum animal encontrado. Crie animais primeiro!")
        return
    
    symptoms_list = [
        '',
        'Agitação',
        'Tosse',
        'Respiração acelerada',
        'Agitação, Tosse',
        'Diarreia',
        'Apatia',
    ]
    
    now = timezone.now()
    created_count = 0
    
    for animal in animals:
        print(f"\n📊 Gerando biometria para {animal.name}...")
        
        # Gerar 10 leituras para cada animal (distribuídas nos últimos 7 dias)
        for i in range(10):
            days_ago = random.randint(0, 7)
            hours_ago = random.randint(0, 23)
            
            reading_time = now - timedelta(days=days_ago, hours=hours_ago)
            
            # Simular variações realistas de biometria
            base_heart_rate = random.randint(60, 85)
            heart_rate = base_heart_rate + random.randint(-10, 20)
            
            base_sleep = random.uniform(4, 7)
            sleep_duration = base_sleep + random.uniform(-1, 1)
            sleep_duration = max(0, min(8, sleep_duration))  # Entre 0 e 8 horas
            
            temperature = 37.5 + random.uniform(-0.5, 1.5)  # Entre 37 e 39°C
            
            symptoms = random.choice(symptoms_list)
            
            # Determinar nível de alerta baseado em valores
            if temperature > 39 or (heart_rate > 100 and sleep_duration < 2):
                alert_level = 'critical'
            elif temperature > 38.5 or (heart_rate > 80 and symptoms):
                alert_level = 'warning'
            else:
                alert_level = 'normal'
            
            reading = BiometricReading.objects.create(
                animal=animal,
                heart_rate=heart_rate,
                sleep_duration=round(sleep_duration, 2),
                body_temperature=round(temperature, 2),
                symptoms=symptoms,
                alert_level=alert_level,
                sensor_battery=random.randint(40, 100),
                reading_timestamp=reading_time,
            )
            
            created_count += 1
            print(f"  ✅ Leitura #{created_count}: {reading.reading_timestamp.strftime('%d/%m/%Y %H:%M')} | "
                  f"FC: {heart_rate} BPM | Sono: {sleep_duration:.1f}h | Temp: {temperature:.1f}°C")
    
    return created_count


def create_critical_alerts():
    """
    Cria alguns alertas críticos para teste.
    """
    animals = Animal.objects.all()[:3]
    
    critical_cases = [
        {
            'title': 'Suspeita de Febre Alta',
            'description': 'Temperatura corporal elevada detectada no sensor.',
            'reason': 'Temperatura acima de 39.5°C (Leitura: 40.2°C)',
            'severity': 'critical',
        },
        {
            'title': 'Deficiência de Sono Severa',
            'description': 'Animal com frequência cardíaca alta e sono inadequado.',
            'reason': 'FC > 100 BPM (118) + Sono < 2h (0.5h)',
            'severity': 'critical',
        },
        {
            'title': 'Temperatura Elevada',
            'description': 'Temperatura corporal acima do normal. Monitorar.',
            'reason': 'Temperatura entre 38.5°C e 39.5°C (Leitura: 39.1°C)',
            'severity': 'high',
        },
    ]
    
    alert_count = 0
    
    for i, animal in enumerate(animals):
        if i >= len(critical_cases):
            break
        
        case = critical_cases[i]
        
        # Pega a leitura mais recente do animal
        latest_reading = BiometricReading.objects.filter(animal=animal).first()
        
        alert = AnimalAlert.objects.create(
            animal=animal,
            title=case['title'],
            description=case['description'],
            reason=case['reason'],
            severity=case['severity'],
            biometric_reading=latest_reading,
            status='active',
        )
        
        alert_count += 1
        print(f"\n🚨 Alerta criado para {animal.name}: {case['title']} ({case['severity'].upper()})")
    
    return alert_count


if __name__ == '__main__':
    print("🌱 Iniciando população de dados de biometria...\n")
    
    # Criar leituras de biometria
    reading_count = create_biometric_data()
    print(f"\n✅ {reading_count} leituras de biometria criadas!")
    
    # Criar alertas críticos
    alert_count = create_critical_alerts()
    print(f"\n✅ {alert_count} alertas críticos criados!")
    
    print("\n🎉 População de dados concluída com sucesso!")
