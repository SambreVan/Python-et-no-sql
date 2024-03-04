from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from faker import Faker
import random

fake = Faker()

uri = "mongodb+srv://Sambre:LeRoiSambre5@cluster0.h7bwuzx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri, server_api=ServerApi('1'))

db = client['Projet']

db["Produits"].delete_many({})

noms_fournisseurs = [fournisseur["nom"] for fournisseur in db["Fournisseurs"].find()]

noms_et_categories = [
    ("Vanille", "Classique"),
    ("Chocolat", "Classique"),
    ("Fraise", "Fruitée"),
    ("Pistache", "Nuts"),
    ("Menthe Chocolat", "Fantaisie"),
]

produits = []
for nom, categorie in noms_et_categories:
    produit = {
        "nom": nom,
        "prix": round(random.uniform(1.5, 5.0), 2),
        "catégorie": categorie,
        "description": fake.text(),
        "fournisseur": random.choice(noms_fournisseurs) if noms_fournisseurs else "Inconnu"
    }
    produits.append(produit)

db["Produits"].insert_many(produits)

print("La collection Produits a été vidée et de nouveaux produits ont été insérés avec leurs fournisseurs.")
