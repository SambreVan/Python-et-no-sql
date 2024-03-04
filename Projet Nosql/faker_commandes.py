from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from faker import Faker
import random

fake = Faker()

uri = "mongodb+srv://Sambre:LeRoiSambre5@cluster0.h7bwuzx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri, server_api=ServerApi('1'))

db = client['Projet']

db["Commandes"].delete_many({})

noms_produits = ["Vanille", "Chocolat", "Fraise", "Pistache", "Menthe chocolat"]
clients = [client["nom"] for client in db["Clients"].find()]

commandes = []
for _ in range(100): 
    commande = {
        "client": random.choice(clients),
        "produit": random.choice(noms_produits),
        "quantité": random.randint(1, 5),
        "date": fake.date_time_between(start_date='-1y', end_date='now')  
    }
    commandes.append(commande)


db["Commandes"].insert_many(commandes)

print("La collection Commandes a été vidée et de nouvelles commandes ont été insérées.")
