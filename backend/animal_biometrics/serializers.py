from rest_framework import serializers
from .models import BiometricReading, AnimalAlert
from animals.models import Animal


class BiometricReadingSerializer(serializers.ModelSerializer):
    """Serializer para leituras de biometria"""
    animal_name = serializers.CharField(source='animal.name', read_only=True)
    alert_emoji = serializers.SerializerMethodField()
    reading_date = serializers.SerializerMethodField()
    
    class Meta:
        model = BiometricReading
        fields = [
            'id',
            'animal',
            'animal_name',
            'heart_rate',
            'sleep_duration',
            'body_temperature',
            'symptoms',
            'alert_level',
            'reading_timestamp',
            'reading_date',
            'sensor_battery',
            'alert_emoji',
        ]
        read_only_fields = ['id', 'reading_timestamp']
    
    def get_alert_emoji(self, obj):
        return obj.get_alert_level_emoji()
    
    def get_reading_date(self, obj):
        return obj.reading_timestamp.strftime('%d/%m/%Y %H:%M')


class AnimalAlertSerializer(serializers.ModelSerializer):
    """Serializer para alertas de animais"""
    animal_name = serializers.CharField(source='animal.name', read_only=True)
    animal_quadrant = serializers.IntegerField(source='animal.quadrant_id', read_only=True)
    severity_emoji = serializers.SerializerMethodField()
    created_date = serializers.SerializerMethodField()
    
    class Meta:
        model = AnimalAlert
        fields = [
            'id',
            'animal',
            'animal_name',
            'animal_quadrant',
            'title',
            'description',
            'reason',
            'severity',
            'severity_emoji',
            'status',
            'biometric_reading',
            'created_at',
            'created_date',
            'acknowledged_at',
            'resolved_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_severity_emoji(self, obj):
        try:
            return obj.get_severity_emoji()
        except Exception:
            return None

    def get_created_date(self, obj):
        if not obj.created_at:
            return None
        return obj.created_at.strftime('%d/%m/%Y %H:%M')


class BiometricReadingDetailSerializer(serializers.ModelSerializer):
    """Serializer detalhado com histórico para gráficos"""
    animal_name = serializers.CharField(source='animal.name', read_only=True)
    alert_emoji = serializers.SerializerMethodField()
    
    class Meta:
        model = BiometricReading
        fields = [
            'id',
            'animal',
            'animal_name',
            'heart_rate',
            'sleep_duration',
            'body_temperature',
            'symptoms',
            'alert_level',
            'reading_timestamp',
            'sensor_battery',
            'alert_emoji',
        ]
    
    def get_alert_emoji(self, obj):
        return obj.get_alert_level_emoji()


class AnimalBiometricSummarySerializer(serializers.Serializer):
    """
    Serializer para resumo de biometria do animal.
    Retorna a última leitura e dados agregados.
    """
    animal_id = serializers.IntegerField()
    animal_name = serializers.CharField()
    
    # Última leitura
    latest_reading = BiometricReadingSerializer()
    
    # Alertas ativos
    active_alerts = AnimalAlertSerializer(many=True)
    active_alerts_count = serializers.IntegerField()
    
    # Estatísticas (últimas 24h)
    avg_heart_rate_24h = serializers.IntegerField(allow_null=True)
    avg_sleep_24h = serializers.DecimalField(max_digits=5, decimal_places=2, allow_null=True)
    avg_temperature_24h = serializers.DecimalField(max_digits=5, decimal_places=2, allow_null=True)
    
    # Contagem de alertas por severidade
    critical_alerts_count = serializers.IntegerField()
    high_alerts_count = serializers.IntegerField()
    medium_alerts_count = serializers.IntegerField()
