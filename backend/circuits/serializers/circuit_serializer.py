from rest_framework import serializers
from circuits.serializers.category_serializer import CategorySerializer
from circuits.serializers.step_serializer import StepSerializer
from circuits.serializers.tag_serializer import TagSerializer
from circuits.models.circuit import  Circuit

class CircuitSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    steps = StepSerializer(many=True, read_only=True)

    class Meta:
        model = Circuit
        fields = [
            'id', 'title', 'description', 'destination',
            'start_date', 'end_date', 'price', 'duration',
            'available_seats', 'status', 'category', 'tags', 'steps',
            'created_at', 'updated_at'
        ]