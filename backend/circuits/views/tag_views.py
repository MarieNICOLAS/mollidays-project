from rest_framework import generics, viewsets, permissions
from circuits.models.tag import Tag
from circuits.serializers.tag_serializer import TagSerializer

class TagListAPIView(generics.ListAPIView):
    queryset = Tag.objects.all().order_by("name")
    serializer_class = TagSerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes =[permissions.IsAdminUser]
