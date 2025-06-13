from pymongo import MongoClient
from datetime import datetime
from django.conf import settings

client = MongoClient("mongodb://localhost:27017/")
db = client["mollidays"]
collection = db["reviews"]

def add_review(user_email, circuit_id, note, comment):
    review = {
        "user_email": user_email,
        "circuit_id": circuit_id,
        "note": note,
        "comment": comment,
        "created_at": datetime.utcnow()
    }
    collection.insert_one(review)
    return review

def get_reviews_for_circuit(circuit_id):
    return list(collection.find({"circuit_id": circuit_id}))
