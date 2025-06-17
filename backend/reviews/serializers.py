from rest_framework import serializers


class ReviewSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    user = serializers.IntegerField(required=False)
    circuit = serializers.IntegerField()
    rating = serializers.IntegerField(min_value=1, max_value=5)
    comment = serializers.CharField(allow_blank=True, required=False)
    created_at = serializers.DateTimeField(read_only=True)