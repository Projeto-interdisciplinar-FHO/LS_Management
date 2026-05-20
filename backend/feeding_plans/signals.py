# backend/feeding_plans/signals.py
import os
from django.db.models.signals import pre_save
from django.dispatch import receiver
from dotenv import load_dotenv

# Importações dos seus modelos para buscar os nomes reais pelos IDs
from feeding_plans.models import FeedingPlan
from weight_history.models import WeightHistory
from animals.models import Animal
from foods.models import Food
from gemini_api.cliente import gerar_alerta_nutricional

load_dotenv()
api_key = os.getenv("API_KEY")

@receiver(pre_save, sender=FeedingPlan)
def feeding_plan_pre_save(sender, instance, **kwargs):
    print("\n[VÍNCULO DETECTADO] -> O sinal pre_save acabou de ser acionado!")
    
    if api_key and len(api_key) > 0:
        print("-> API_KEY encontrada com sucesso. Acionando o Gemini...")
        
        try:
            animal_obj = Animal.objects.get(id=instance.animal_id)
            food_obj = Food.objects.get(id=instance.food_id)
            ultimo_peso = WeightHistory.objects.filter(animal=animal_obj).order_by('-weighing_date').first()
            peso_atual = f"{ultimo_peso.weight}" if ultimo_peso else "Não informado"
            
            print(f"-> Dados validados. Chamando Gemini para o animal: {animal_obj.name}")
            
            alerta_ia = gerar_alerta_nutricional(
                animal_name=animal_obj.name,
                alimento=food_obj.name,
                periodicidade=instance.periodicity,
                peso_atual=peso_atual
            )
            
            print(f"-> Resposta recebida do Gemini com sucesso!")
            instance.alerta_nutricional_ia = alerta_ia
            
        except Exception as e:
            print(f"-> ERRO AO EXECUTAR O SINAL: {str(e)}")
            instance.alerta_nutricional_ia = f"Erro no processamento dos dados do sinal: {str(e)}"
    else:
        print("-> ERRO CRÍTICO: A API_KEY não foi encontrada dentro do arquivo .env ou o arquivo .env está na pasta errada!")
        instance.alerta_nutricional_ia = "Chave de API do Gemini não configurada no servidor."