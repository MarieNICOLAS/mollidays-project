from rest_framework import generics
from circuits.models.tag import Tag
from circuits.serializers.tag_serializer import TagSerializer

class TagListAPIView(generics.ListAPIView):
    queryset = Tag.objects.all().order_by("name")
    serializer_class = TagSerializer