from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum
from milk_production_history.models import MilkProductionHistory
from milk_production_history.serializers import MilkProductionHistorySerializer
from notifications.models import Notification


class MilkProductionHistoryCreateListView(generics.ListCreateAPIView):
    queryset = MilkProductionHistory.objects.all()
    serializer_class = MilkProductionHistorySerializer
    
    def perform_create(self, serializer):
        """Cria o registro de ordenha e registra uma notificação"""
        milk = serializer.save()
        
        # Cria notificação para o administrador
        message = f"Operador registrou ordenha: {milk.animal.name} (#{milk.animal.register_number}) - {milk.milk_production}L"
        Notification.create_notification(
            message=message,
            notification_type='milk',
            animal=milk.animal
        )

class MilkProductionHistoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = MilkProductionHistory.objects.all()
    serializer_class = MilkProductionHistorySerializer


class MilkProductionHistoryByAnimalView(APIView):
    """Retorna histórico de produção de leite para um animal específico com resumo de estatísticas"""
    
    def get(self, request, animal_id):
        try:
            # Buscar todo o histórico do animal
            historico = MilkProductionHistory.objects.filter(
                animal_id=animal_id
            ).order_by('-production_date')
            
            # Serializar histórico
            serializer = MilkProductionHistorySerializer(historico, many=True)
            
            # Calcular resumo
            hoje = timezone.now().date()
            semana_atras = hoje - timedelta(days=7)
            mes_atras = hoje - timedelta(days=30)
            
            # Última ordenha
            ultima_ordenha = historico.first()
            
            # Totais
            total_semana = historico.filter(
                production_date__gte=semana_atras
            ).aggregate(total=Sum('milk_production'))['total'] or 0
            
            total_mes = historico.filter(
                production_date__gte=mes_atras
            ).aggregate(total=Sum('milk_production'))['total'] or 0
            
            total_geral = historico.aggregate(total=Sum('milk_production'))['total'] or 0
            
            # Contar quantidade de ordenhas
            quantidade_ordenhas = historico.count()
            
            response_data = {
                'historico': serializer.data,
                'resumo': {
                    'ultima_ordenha': {
                        'milk_production': ultima_ordenha.milk_production if ultima_ordenha else 0,
                        'production_date': ultima_ordenha.production_date if ultima_ordenha else None
                    } if ultima_ordenha else None,
                    'total_semana': total_semana,
                    'total_mes': total_mes,
                    'total_geral': total_geral,
                    'quantidade_ordenhas': quantidade_ordenhas
                }
            }
            
            return Response(response_data)
        except Exception as e:
            return Response({'error': str(e)}, status=400)
