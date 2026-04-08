from rest_framework import serializers
from purpose_types.models import PurposeType

class PurposeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurposeType
        fields = '__all__'