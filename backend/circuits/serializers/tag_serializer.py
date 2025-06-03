from dataclasses import field
from rest_framework import serializers
from circuits.models.tag import Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']