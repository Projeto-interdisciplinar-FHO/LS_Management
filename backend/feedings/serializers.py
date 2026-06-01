from rest_framework import serializers
from feedings.models import Feeding


class FeedingSerializer(serializers.ModelSerializer):
    animal_name = serializers.SerializerMethodField(read_only=True)
    animal_register = serializers.SerializerMethodField(read_only=True)
    feed_name = serializers.SerializerMethodField(read_only=True)
    date_fed = serializers.SerializerMethodField(read_only=True)
    quantity = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Feeding
        fields = '__all__'

    def get_animal_name(self, obj):
        return obj.animal.name if obj.animal else None

    def get_animal_register(self, obj):
        return obj.animal.register_number if obj.animal else None

    def get_feed_name(self, obj):
        return obj.food.name if obj.food else None

    def get_date_fed(self, obj):
        if not obj.feeding_time:
            return None
        return obj.feeding_time.strftime('%Y-%m-%d')

    def get_quantity(self, obj):
        return obj.meal_weight
