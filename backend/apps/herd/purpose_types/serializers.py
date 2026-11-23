from rest_framework import serializers
from apps.herd.purpose_types.models import PurposeType

class PurposeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurposeType
        fields = '__all__'