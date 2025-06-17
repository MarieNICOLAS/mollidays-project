from datetime import datetime
from bson import ObjectId
from pymongo import MongoClient
from django.conf import settings

# Initialize Mongo connection using settings
client = MongoClient(settings.MONGO_CONNECTION_STRING)
db = client[settings.MONGO_DB_NAME]
collection = db["reviews"]


def serialize(review):
    """Convert Mongo review document to JSON serializable dict."""
    review["id"] = str(review.pop("_id"))
    review["created_at"] = review["created_at"].isoformat()
    return review


def create_review(user_id, circuit_id, rating, comment):
    review = {
        "user": user_id,
        "circuit": circuit_id,
        "rating": rating,
        "comment": comment,
        "created_at": datetime.utcnow(),
    }
    result = collection.insert_one(review)
    review["id"] = str(result.inserted_id)
    review.pop("_id", None)
    review["created_at"] = review["created_at"].isoformat()
    return review


def list_reviews(filter_query=None):
    query = filter_query or {}
    reviews = []
    for r in collection.find(query):
        reviews.append(serialize(r))
    return reviews


def get_review(review_id):
    data = collection.find_one({"_id": ObjectId(review_id)})
    if not data:
        return None
    return serialize(data)


def update_review(review_id, data):
    update_data = {k: v for k, v in data.items() if k in {"rating", "comment"}}
    if not update_data:
        return get_review(review_id)
    result = collection.update_one({"_id": ObjectId(review_id)}, {"$set": update_data})
    if result.matched_count:
        return get_review(review_id)
    return None


def delete_review(review_id):
    result = collection.delete_one({"_id": ObjectId(review_id)})
    return result.deleted_count > 0


def get_reviews_for_circuit(circuit_id):
    return list_reviews({"circuit": circuit_id})