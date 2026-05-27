from rest_framework import generics, status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import timedelta
from django.utils import timezone
from django.db.models import Avg, Max, Min
from weight_history.models import WeightHistory
from weight_history.serializers import WeightHistorySerializer
from notifications.models import Notification
from animals.models import Animal

class WeightHistoryCreateListView(generics.ListCreateAPIView):
    queryset = WeightHistory.objects.all()
    serializer_class = WeightHistorySerializer
    
    def perform_create(self, serializer):
        """Cria o registro de peso e registra uma notificação"""
        weight = serializer.save()
        
        # Cria notificação para o administrador
        message = f"Operador registrou pesagem: {weight.animal.name} (#{weight.animal.register_number}) - {weight.weight}kg"
        Notification.create_notification(
            message=message,
            notification_type='weight',
            animal=weight.animal
        )
    
    def create(self, request, *args, **kwargs):
        """Sobrescreve create para melhorar tratamento de erros"""
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except serializers.ValidationError as e:
            return Response(
                {'error': str(e.detail) if hasattr(e, 'detail') else str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Animal.DoesNotExist:
            return Response(
                {'error': 'Animal não encontrado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': f'Erro ao registrar peso: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

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