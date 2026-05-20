from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import timedelta
from django.utils import timezone
from django.db.models import Avg, Max, Min
from weight_history.models import WeightHistory
from weight_history.serializers import WeightHistorySerializer

class WeightHistoryCreateListView(generics.ListCreateAPIView):
    queryset = WeightHistory.objects.all()
    serializer_class = WeightHistorySerializer

class WeightHistoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = WeightHistory.objects.all()
    serializer_class = WeightHistorySerializer


class WeightHistoryByAnimalView(APIView):
    """Retorna histórico de peso para um animal específico com resumo de estatísticas"""
    
    def get(self, request, animal_id):
        try:
            # Buscar todo o histórico do animal
            historico = WeightHistory.objects.filter(
                animal_id=animal_id
            ).order_by('-weighing_date')
            
            # Serializar histórico
            serializer = WeightHistorySerializer(historico, many=True)
            
            # Calcular resumo
            hoje = timezone.now().date()
            semana_atras = hoje - timedelta(days=7)
            mes_atras = hoje - timedelta(days=30)
            
            # Última pesagem
            ultima_pesagem = historico.first()
            
            # Estatísticas
            total_pesagens = historico.count()
            peso_medio = historico.aggregate(media=Avg('weight'))['media'] or 0
            peso_maximo = historico.aggregate(maximo=Max('weight'))['maximo'] or 0
            peso_minimo = historico.aggregate(minimo=Min('weight'))['minimo'] or 0
            
            # Última pesagem e penúltima para calcular ganho
            ultima_pesagem_obj = historico.first()
            penultima_pesagem = historico.exclude(id=ultima_pesagem_obj.id).first() if ultima_pesagem_obj else None
            ganho_peso = 0
            if ultima_pesagem_obj and penultima_pesagem:
                ganho_peso = float(ultima_pesagem_obj.weight) - float(penultima_pesagem.weight)
            
            response_data = {
                'historico': serializer.data,
                'resumo': {
                    'ultima_pesagem': {
                        'weight': float(ultima_pesagem.weight) if ultima_pesagem else 0,
                        'weighing_date': ultima_pesagem.weighing_date if ultima_pesagem else None
                    } if ultima_pesagem else None,
                    'peso_medio': float(peso_medio),
                    'peso_maximo': float(peso_maximo),
                    'peso_minimo': float(peso_minimo),
                    'total_pesagens': total_pesagens,
                    'ganho_peso_recente': ganho_peso
                }
            }
            
            return Response(response_data)
        except Exception as e:
            return Response({'error': str(e)}, status=400)
    serializer_class = WeightHistorySerializer