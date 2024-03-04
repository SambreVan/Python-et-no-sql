from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from faker import Faker

fake = Faker()

uri = "mongodb+srv://Sambre:LeRoiSambre5@cluster0.h7bwuzx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri, server_api=ServerApi('1'))

db = client['Projet']

db["Clients"].delete_many({})

clients = []
for _ in range(100):  
    client = {
        "nom": fake.name(),
        "adresse": fake.address(),
        "email": fake.email(),
        "téléphone": fake.phone_number()
    }
    clients.append(client)

db["Clients"].insert_many(clients)

print("La collection Clients a été vidée et de nouveaux clients ont été insérés.")
