from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://Sambre:LeRoiSambre5@cluster0.h7bwuzx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri, server_api=ServerApi('1'))

db = client['Projet']

db["Catégories"].delete_many({})

categories_de_glaces = [
    "Vanille", "Chocolat", "Fraise", "Pistache", 
    "Menthe chocolat", "Caramel beurre salé", 
    "Noix de coco", "Café", "Citron", "Mangue",
    "Sorbet", "Crème glacée", "Yaourt glacé", "Glace végane"
]

db["Catégories"].insert_many([{"nom": categorie} for categorie in categories_de_glaces])

print("La collection Catégories a été vidée et de nouvelles catégories de glaces ont été insérées.")
