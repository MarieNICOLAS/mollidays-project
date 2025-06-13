from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from reviews.review_service import add_review, get_reviews_for_circuit

class AddReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        note = data.get("note")
        comment = data.get("comment")
        circuit_id = data.get("circuit_id")

        if not (note and circuit_id):
            return Response({"error": "Note et circuit_id requis"}, status=400)

        review = add_review(request.user.email, int(circuit_id), int(note), comment)
        return Response({"message": "Avis ajouté", "review": str(review)}, status=201)

class CircuitReviewListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, circuit_id):
        reviews = get_reviews_for_circuit(int(circuit_id))
        for r in reviews:
            r["_id"] = str(r["_id"])
            r["created_at"] = r["created_at"].isoformat()
        return Response(reviews)
