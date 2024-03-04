from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb+srv://Sambre:LeRoiSambre5@cluster0.h7bwuzx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['Projet']

def transform_mongo_doc(doc):
    doc["_id"] = str(doc["_id"])
    return doc

@app.route('/')
def index():
    return "GLACE API"


# Liste des Produits d'une Catégorie Spécifique
@app.route('/produits/categorie/<categorie>', methods=['GET'])
def get_produits_par_categorie(categorie):
    produits = db["Produits"].find({"catégorie": categorie})
    return jsonify([transform_mongo_doc(produit) for produit in produits])
#http://127.0.0.1:5000/produits/categorie/Classique

# Liste des Produits d'un Fournisseur Spécifique
@app.route('/produits/fournisseur/<nom_fournisseur>', methods=['GET'])
def get_produits_par_fournisseur(nom_fournisseur):
    produits = db["Produits"].find({"fournisseur": nom_fournisseur})
    return jsonify([transform_mongo_doc(produit) for produit in produits])
#http://127.0.0.1:5000/produits/fournisseur/Montes,%20Huang%20and%20George

#commandes par client
@app.route('/commandes/client/<nom_client>', methods=['GET'])
def get_commandes_par_client(nom_client):
    commandes = db["Commandes"].find({"client": nom_client})
    return jsonify([transform_mongo_doc(commande) for commande in commandes])
#http://127.0.0.1:5000/commandes/client/Andrew%20Adams

# Produits les Plus Vendus
@app.route('/produits/plus_vendus', methods=['GET'])
def get_produits_plus_vendus():
    produits = db["Produits"].find().sort("quantité_vendue", -1).limit(10)
    return jsonify([transform_mongo_doc(produit) for produit in produits])
#http://127.0.0.1:5000/produits/plus_vendus

# Produits les Moins Vendus
@app.route('/produits/moins_vendus', methods=['GET'])
def get_produits_moins_vendus():
    ventes_produits = db["Commandes"].aggregate([
        {"$group": {
            "_id": "$produit",
            "total_vendu": {"$sum": "$quantité"}
        }},
        {"$sort": {"total_vendu": 1}},  
        {"$limit": 10},  
        {"$lookup": {  
            "from": "Produits",
            "localField": "_id",
            "foreignField": "nom",
            "as": "details_produit"
        }},
        {"$unwind": "$details_produit"}  
    ])

    resultats = []
    for item in ventes_produits:
        produit = item["details_produit"]
        produit["total_vendu"] = item["total_vendu"]
        resultats.append(transform_mongo_doc(produit))

    return jsonify(resultats)
#http://127.0.0.1:5000/produits/moins_vendus

# Détails des Commandes Récentes
@app.route('/commandes/recentes', methods=['GET'])
def get_commandes_recentes():
    commandes = db["Commandes"].find().sort("date", -1).limit(10)
    return jsonify([transform_mongo_doc(commande) for commande in commandes])
#http://127.0.0.1:5000/commandes/recentes

# Catégories les Plus Populaires
@app.route('/categories/populaires', methods=['GET'])
def get_categories_populaires():
    categories = db["Commandes"].aggregate([
        {"$lookup": {
            "from": "Produits",
            "localField": "produit",
            "foreignField": "nom",
            "as": "infos_produit"
        }},
        {"$unwind": "$infos_produit"},
        {"$group": {"_id": "$infos_produit.catégorie", "total_vendu": {"$sum": "$quantité"}}},
        {"$sort": {"total_vendu": -1}}
    ])
    return jsonify([categorie for categorie in categories])
#http://127.0.0.1:5000/categories/populaires


# Produits Jamais Commandés
@app.route('/produits/jamais_commandes', methods=['GET'])
def get_produits_jamais():
    commandes = db["Commandes"].distinct("produit")
    produits = db["Produits"].find({"nom": {"$nin": commandes}})
    return jsonify([transform_mongo_doc(produit) for produit in produits])
#http://127.0.0.1:5000/produits/jamais_commandes

# Ventes Totales par Catégorie
@app.route('/categories/ventes_total', methods=['GET'])
def get_ventes_par_categorie():
    ventes = db["Commandes"].aggregate([
        {"$lookup": {
            "from": "Produits",
            "localField": "produit",
            "foreignField": "nom",
            "as": "info_produit"
        }},
        {"$unwind": "$info_produit"},
        {"$group": {
            "_id": "$info_produit.catégorie",
            "total_vendu": {"$sum": "$quantité"}
        }},
        {"$sort": {"total_vendu": -1}}
    ])
    return jsonify([vente for vente in ventes])
#http://127.0.0.1:5000/categories/ventes_total

# Nombre de Produits par Catégorie
@app.route('/categories/nombre_produits', methods=['GET'])
def get_nombre_produits_par_categorie():
    categories = db["Produits"].aggregate([
        {"$group": {
            "_id": "$catégorie",
            "nombre_produits": {"$sum": 1}
        }},
        {"$sort": {"nombre_produits": -1}}
    ])
    return jsonify([categorie for categorie in categories])
#http://127.0.0.1:5000/categories/nombre_produits


# Fournisseurs d'un Produit Spécifique
@app.route('/fournisseurs/produit/<nom_produit>', methods=['GET'])
def get_fournisseurs_par_produit(nom_produit):
    fournisseurs = db["Produits"].find({"nom": nom_produit}, {"fournisseur": 1})
    return jsonify([transform_mongo_doc(fournisseur) for fournisseur in fournisseurs])
#http://127.0.0.1:5000/fournisseurs/produit/Chocolat


if __name__ == '__main__':
    app.run(debug=True)
