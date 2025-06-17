from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status

from .mongo_service import (
    create_review,
    list_reviews,
    get_review,
    update_review,
    delete_review,
    get_reviews_for_circuit,
)
from .serializers import ReviewSerializer


class ReviewListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        reviews = list_reviews()
        return Response(reviews)

    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            review = create_review(
                request.user.id,
                data["circuit"],
                data["rating"],
                data.get("comment", ""),
            )
            return Response(review, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, review_id):
        review = get_review(review_id)
        if review:
            return Response(review)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, review_id):
        serializer = ReviewSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            review = update_review(review_id, serializer.validated_data)
            if review:
                return Response(review)
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, review_id):
        if delete_review(review_id):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


class CircuitReviewListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, circuit_id):
        return Response(get_reviews_for_circuit(circuit_id))