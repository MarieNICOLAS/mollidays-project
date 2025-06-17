from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["mollidays"]
collection = db["reviews"]

# Exemple de données
review = {
    "user": 5,  # ID du user jsmith@gmail.com
    "circuit": 3,
    "rating": 4,
    "comment": "Très bon séjour, bien organisé et enrichissant.",
    "created_at": datetime.utcnow()
}

result = collection.insert_one(review)
print("✅ Review ajoutée avec l'ID :", result.inserted_id)
