from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from faker import Faker

fake = Faker()

uri = "mongodb+srv://Sambre:LeRoiSambre5@cluster0.h7bwuzx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri, server_api=ServerApi('1'))

db = client['Projet']

db["Fournisseurs"].delete_many({})

fournisseurs = []
for _ in range(100):  
    fournisseur = {
        "nom": fake.company(),
        "adresse": fake.address()
    }
    fournisseurs.append(fournisseur)

db["Fournisseurs"].insert_many(fournisseurs)

print("La collection Fournisseurs a été vidée et de nouveaux fournisseurs ont été insérés.")
