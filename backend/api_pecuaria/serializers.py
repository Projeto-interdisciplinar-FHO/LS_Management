from rest_framework import serializers
from gestao.models import Bovino, Historico

class HistoricoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historico
        fields = ['animal', 'tipo', 'valor', 'data', 'sintomas']

class BovinoSerializer(serializers.ModelSerializer):
    historicos = HistoricoSerializer(many=True, read_only=True)

    class Meta:
        model = Bovino
        fields = ['id', 'rfid_tag', 'nome', 'raca', 'status', 'historicos']