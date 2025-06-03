from rest_framework import serializers
from circuits.models.step import Step

class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = ['id', 'title', 'description', 'order', 'duration_hours']