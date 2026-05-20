from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone
from django.db.models import Avg, Q, Count
from datetime import timedelta

from .models import BiometricReading, AnimalAlert
from .serializers import (
    BiometricReadingSerializer,
    AnimalAlertSerializer,
    BiometricReadingDetailSerializer,
    AnimalBiometricSummarySerializer
)
from animals.models import Animal


class BiometricReadingPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 100


class BiometricReadingViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gerenciar leituras de biometria de animais.
    
    GET /api/biometric-readings/
        - Lista todas as leituras de biometria
    
    GET /api/biometric-readings/?animal_id=1
        - Lista leituras de um animal específico
    
    POST /api/biometric-readings/
        - Cria uma nova leitura (simula recebimento de dados do sensor)
    
    GET /api/biometric-readings/by-animal/{animal_id}/
        - Resumo de biometria de um animal específico (para AnimalDetailView)
    
    GET /api/biometric-readings/history/{animal_id}/?days=7
        - Histórico de leituras para gráficos (últimas N dias)
    """
    queryset = BiometricReading.objects.all()
    serializer_class = BiometricReadingSerializer
    pagination_class = BiometricReadingPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['animal__name', 'animal__register_number']
    ordering_fields = ['reading_timestamp', 'alert_level']
    ordering = ['-reading_timestamp']
    
    def get_queryset(self):
        queryset = BiometricReading.objects.all()
        
        # Filtro por animal específico
        animal_id = self.request.query_params.get('animal_id', None)
        if animal_id is not None:
            queryset = queryset.filter(animal_id=animal_id)
        
        # Filtro por nível de alerta
        alert_level = self.request.query_params.get('alert_level', None)
        if alert_level is not None:
            queryset = queryset.filter(alert_level=alert_level)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def by_animal(self, request):
        """
        GET /api/biometric-readings/by-animal/{animal_id}/
        Retorna um resumo da biometria de um animal (última leitura + alertas ativos).
        """
        animal_id = request.query_params.get('animal_id', None)
        
        if animal_id is None:
            return Response(
                {'error': 'animal_id é obrigatório'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            animal = Animal.objects.get(id=animal_id)
        except Animal.DoesNotExist:
            return Response(
                {'error': f'Animal com ID {animal_id} não encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Última leitura
        latest_reading = BiometricReading.objects.filter(
            animal_id=animal_id
        ).first()
        
        # Alertas ativos
        active_alerts = AnimalAlert.objects.filter(
            animal_id=animal_id,
            status__in=['active', 'acknowledged']
        )
        
        # Estatísticas das últimas 24h
        now = timezone.now()
        readings_24h = BiometricReading.objects.filter(
            animal_id=animal_id,
            reading_timestamp__gte=now - timedelta(hours=24)
        )
        
        avg_heart_rate = readings_24h.aggregate(Avg('heart_rate'))['heart_rate__avg']
        avg_sleep = readings_24h.aggregate(Avg('sleep_duration'))['sleep_duration__avg']
        avg_temperature = readings_24h.aggregate(Avg('body_temperature'))['body_temperature__avg']
        
        # Contagem de alertas por severidade
        alert_counts = active_alerts.aggregate(
            critical=Count('id', filter=Q(severity='critical')),
            high=Count('id', filter=Q(severity='high')),
            medium=Count('id', filter=Q(severity='medium')),
            low=Count('id', filter=Q(severity='low')),
        )
        
        data = {
            'animal_id': animal.id,
            'animal_name': animal.name,
            'latest_reading': BiometricReadingSerializer(latest_reading).data if latest_reading else None,
            'active_alerts': AnimalAlertSerializer(active_alerts, many=True).data,
            'active_alerts_count': active_alerts.count(),
            'avg_heart_rate_24h': int(avg_heart_rate) if avg_heart_rate else None,
            'avg_sleep_24h': float(avg_sleep) if avg_sleep else None,
            'avg_temperature_24h': float(avg_temperature) if avg_temperature else None,
            'critical_alerts_count': alert_counts['critical'],
            'high_alerts_count': alert_counts['high'],
            'medium_alerts_count': alert_counts['medium'],
            'low_alerts_count': alert_counts['low'],
        }
        
        return Response(data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def history(self, request):
        """
        GET /api/biometric-readings/history/?animal_id=1&days=7
        Retorna histórico de leituras para gráficos.
        """
        animal_id = request.query_params.get('animal_id', None)
        days = int(request.query_params.get('days', 7))
        
        if animal_id is None:
            return Response(
                {'error': 'animal_id é obrigatório'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Filtrar leituras dos últimos N dias
        now = timezone.now()
        readings = BiometricReading.objects.filter(
            animal_id=animal_id,
            reading_timestamp__gte=now - timedelta(days=days)
        ).order_by('reading_timestamp')
        
        serializer = BiometricReadingDetailSerializer(readings, many=True)
        
        return Response({
            'animal_id': animal_id,
            'days': days,
            'total_readings': readings.count(),
            'readings': serializer.data,
        }, status=status.HTTP_200_OK)
    
    def perform_create(self, serializer):
        """Hook para quando uma leitura é criada"""
        biometric_reading = serializer.save()
        
        # Disparar análise automática de alertas
        check_and_create_alerts(biometric_reading)


class AnimalAlertViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gerenciar alertas de animais.
    
    GET /api/animal-alerts/
        - Lista todos os alertas
    
    GET /api/animal-alerts/?animal_id=1
        - Alertas de um animal específico
    
    GET /api/animal-alerts/critical/
        - Todos os alertas críticos e ativos (para Dashboard)
    
    POST /api/animal-alerts/{id}/acknowledge/
        - Marca um alerta como reconhecido
    
    POST /api/animal-alerts/{id}/resolve/
        - Marca um alerta como resolvido
    """
    queryset = AnimalAlert.objects.all()
    serializer_class = AnimalAlertSerializer
    pagination_class = BiometricReadingPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['animal__name', 'title', 'description']
    ordering_fields = ['created_at', 'severity']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = AnimalAlert.objects.all()
        
        # Filtro por animal específico
        animal_id = self.request.query_params.get('animal_id', None)
        if animal_id is not None:
            queryset = queryset.filter(animal_id=animal_id)
        
        # Filtro por status
        status_filter = self.request.query_params.get('status', None)
        if status_filter is not None:
            queryset = queryset.filter(status=status_filter)
        
        # Filtro por severidade
        severity = self.request.query_params.get('severity', None)
        if severity is not None:
            queryset = queryset.filter(severity=severity)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def critical(self, request):
        """
        GET /api/animal-alerts/critical/
        Retorna alertas críticos e ativos para o Dashboard do Operador.
        """
        critical_alerts = AnimalAlert.objects.filter(
            severity__in=['critical', 'high'],
            status__in=['active', 'acknowledged']
        ).select_related('animal').order_by('-created_at')[:10]
        
        serializer = AnimalAlertSerializer(critical_alerts, many=True)
        
        return Response({
            'total_critical': critical_alerts.count(),
            'alerts': serializer.data,
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def by_animal(self, request):
        """
        GET /api/animal-alerts/by-animal/?animal_id=1
        Retorna alertas de um animal específico.
        """
        animal_id = request.query_params.get('animal_id', None)
        
        if animal_id is None:
            return Response(
                {'error': 'animal_id é obrigatório'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        alerts = AnimalAlert.objects.filter(animal_id=animal_id).order_by('-created_at')
        serializer = AnimalAlertSerializer(alerts, many=True)
        
        return Response({
            'animal_id': animal_id,
            'total_alerts': alerts.count(),
            'alerts': serializer.data,
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def acknowledge(self, request, pk=None):
        """
        POST /api/animal-alerts/{id}/acknowledge/
        Marca o alerta como reconhecido pelo operador.
        """
        alert = self.get_object()
        alert.acknowledge()
        
        serializer = AnimalAlertSerializer(alert)
        return Response(
            {'message': 'Alerta reconhecido', 'alert': serializer.data},
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        """
        POST /api/animal-alerts/{id}/resolve/
        Marca o alerta como resolvido.
        """
        alert = self.get_object()
        alert.resolve()
        
        serializer = AnimalAlertSerializer(alert)
        return Response(
            {'message': 'Alerta resolvido', 'alert': serializer.data},
            status=status.HTTP_200_OK
        )


def check_and_create_alerts(biometric_reading):
    """
    Função que analisa uma leitura de biometria e dispara alertas automáticos.
    Regras de alerta:
    - Frequência cardíaca > 100 BPM + Sono < 2h = CRÍTICO
    - Frequência cardíaca > 80 BPM + Sintomas detectados = ALTO
    - Temperatura > 39.5°C = CRÍTICO
    - Temperatura > 38.5°C = ALTO
    - Sono < 1h em 24h = MÉDIO
    """
    animal = biometric_reading.animal
    animal_id = animal.id
    
    # Verificar se já existe alerta ativo recente (últimas 2 horas)
    recent_alert = AnimalAlert.objects.filter(
        animal_id=animal_id,
        status='active',
        created_at__gte=timezone.now() - timedelta(hours=2)
    ).first()
    
    if recent_alert:
        # Se já existe alerta ativo recente, não criar novo
        return
    
    # Regra 1: Temperatura elevada = CRÍTICO
    if biometric_reading.body_temperature and biometric_reading.body_temperature > 39.5:
        AnimalAlert.objects.create(
            animal=animal,
            title='Febre Alta Detectada',
            description=f'Temperatura corporal de {biometric_reading.body_temperature}°C detectada.',
            reason=f'Temperatura acima de 39.5°C (Leitura: {biometric_reading.body_temperature}°C)',
            severity='critical',
            biometric_reading=biometric_reading,
            status='active'
        )
        return
    
    # Regra 2: Temperatura elevada = ALTO
    if biometric_reading.body_temperature and biometric_reading.body_temperature > 38.5:
        AnimalAlert.objects.create(
            animal=animal,
            title='Temperatura Elevada',
            description=f'Temperatura corporal de {biometric_reading.body_temperature}°C. Monitorar.',
            reason=f'Temperatura entre 38.5°C e 39.5°C (Leitura: {biometric_reading.body_temperature}°C)',
            severity='high',
            biometric_reading=biometric_reading,
            status='active'
        )
        return
    
    # Regra 3: Frequência cardíaca alta + sem dormir = CRÍTICO
    if biometric_reading.heart_rate > 100 and biometric_reading.sleep_duration < 2:
        AnimalAlert.objects.create(
            animal=animal,
            title='Suspeita de Febre/Agitação Severa',
            description=f'Frequência cardíaca {biometric_reading.heart_rate} BPM + Sono {biometric_reading.sleep_duration}h.',
            reason=f'FC > 100 BPM ({biometric_reading.heart_rate}) + Sono < 2h ({biometric_reading.sleep_duration}h)',
            severity='critical',
            biometric_reading=biometric_reading,
            status='active'
        )
        return
    
    # Regra 4: Frequência cardíaca alta + Sintomas = ALTO
    if biometric_reading.heart_rate > 80 and biometric_reading.symptoms:
        AnimalAlert.objects.create(
            animal=animal,
            title='Animação Elevada com Sintomas',
            description=f'FC {biometric_reading.heart_rate} BPM + Sintomas: {biometric_reading.symptoms}',
            reason=f'FC > 80 BPM ({biometric_reading.heart_rate}) + Sintomas detectados',
            severity='high',
            biometric_reading=biometric_reading,
            status='active'
        )
        return
    
    # Regra 5: Pouco sono = MÉDIO
    if biometric_reading.sleep_duration < 1:
        AnimalAlert.objects.create(
            animal=animal,
            title='Déficit de Sono',
            description=f'Animal dormiu menos de 1 hora nas últimas 24h.',
            reason=f'Sono inferior a 1h (Leitura: {biometric_reading.sleep_duration}h)',
            severity='medium',
            biometric_reading=biometric_reading,
            status='active'
        )
        return
