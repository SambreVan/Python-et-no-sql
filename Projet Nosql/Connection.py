from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Votre URI de connexion MongoDB
uri = "mongodb+srv://Sambre:LeRoiSambre5@cluster0.h7bwuzx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Créer un client MongoDB
client = MongoClient(uri, server_api=ServerApi('1'))

# Accéder à la base de données 'Projet'
db = client['Projet']

# Créer des collections pour le projet de catalogue de produits de glaces
collections = ["Produits", "Catégories", "Fournisseurs", "Clients", "Commandes"]

for collection in collections:
    db.create_collection(collection)

# Insérer des données d'exemple dans chaque collection
db["Produits"].insert_many([
    {"nom": "Glace Vanille", "prix": 2.99, "catégorie": "Vanille"},
    {"nom": "Glace Chocolat", "prix": 3.49, "catégorie": "Chocolat"}
])

db["Catégories"].insert_many([
    {"nom": "Vanille"},
    {"nom": "Chocolat"}
])

db["Fournisseurs"].insert_one({"nom": "Fournisseur A", "adresse": "123 Rue A"})

db["Clients"].insert_one({"nom": "Client A", "adresse": "456 Rue B"})

db["Commandes"].insert_one({"produit": "Glace Vanille", "quantité": 10, "client": "Client A"})

print("Collections créées et données d'exemple insérées avec succès.")
