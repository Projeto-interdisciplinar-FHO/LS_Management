from rest_framework import serializers
from gestao.models import Bovino, Historico
from django.utils import timezone

class AnaliseCompletaSerializer(serializers.ModelSerializer):
    ganho_medio_diario = serializers.SerializerMethodField()
    alerta_saude = serializers.SerializerMethodField()
    pode_vender = serializers.SerializerMethodField() #periodo de carência

    ultimo_peso = serializers.SerializerMethodField()
    ultima_producao_leite = serializers.SerializerMethodField()
    ultimo_sono = serializers.SerializerMethodField()
    ultimo_bpm = serializers.SerializerMethodField()

    class Meta:
        model = Bovino
        fields = [
            'rfid_tag', 'nome', 'raca', 'status', 
            'ultimo_peso', 'ganho_medio_diario', 
            'ultima_producao_leite', 
            'ultimo_sono', 
            'ultimo_bpm', 
            'alerta_saude', 'pode_vender'
        ]

    def get_ultimo_peso(self, obj):
        registro = obj.historicos.filter(tipo='PESO').first()
        return registro.valor if registro else 0

    def get_ultima_producao_leite(self, obj):
        registro = obj.historicos.filter(tipo='LEITE').first()
        return registro.valor if registro else 0

    def get_ultimo_sono(self, obj):
        registro = obj.historicos.filter(tipo='SONO').first()
        return registro.valor if registro else 0

    def get_ultimo_bpm(self, obj):
        registro = obj.historicos.filter(tipo='BPM').first()
        return registro.valor if registro else 0

    def get_ganho_medio_diario(self, obj):
        pesos = obj.historicos.filter(tipo='PESO')[:2]
        if pesos.count() < 2: return 0
        
        p1, p2 = pesos[0], pesos[1]
        dias = (p1.data - p2.data).days
        if dias <= 0: return 0 
        
        return round((p1.valor - p2.valor) / dias, 3)

    def get_alerta_saude(self, obj):
        ultimo_bpm = obj.historicos.filter(tipo='BPM').first()
        ultimo_sintoma = obj.historicos.exclude(sintomas__isnull=True).exclude(sintomas="").first()

        if ultimo_bpm and ultimo_bpm.valor > 100:
            return f"ALERTA: Frequência Cardíaca Alta ({ultimo_bpm.valor} BPM)!"

        if ultimo_sintoma:
            return f"ALERTA: Sintomas detectados: {ultimo_sintoma.sintomas}"

        return "Normal"

    def get_pode_vender(self, obj):
        vacina = obj.historicos.filter(tipo='VACINA').first()
        if not vacina: return True
        return (timezone.now() - vacina.data).days >= 30