from dataclasses import fields
from rest_framework import serializers
from circuits.models.category import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']