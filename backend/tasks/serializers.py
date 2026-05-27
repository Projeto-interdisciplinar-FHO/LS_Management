from rest_framework import serializers
from tasks.models import Task

class TaskSerializer(serializers.ModelSerializer):
    animal_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'priority', 'due_date', 'completed', 'animal', 'animal_name', 'created_at', 'updated_at']
    
    def get_animal_name(self, obj):
        return obj.animal.name if obj.animal else None
