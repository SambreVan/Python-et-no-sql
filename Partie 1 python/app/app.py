import tkinter as tk
from gui import *
from database import Database
from internet_data import InternetDataFetcher

def main():
    # Initialisation de la fenêtre principale
    root = tk.Tk()
    root.title("Project Cat Image Viewer")


    # Initialisation de la base de données
    db = Database('database.db')

    # Créer la table si elle n'existe pas
    db.create_table()

    fetcher = InternetDataFetcher("https://api.thecatapi.com/v1/images/search?limit=10")
    json_data = fetcher.fetch_json()

    if json_data:
        for item in json_data:
            db.insert_cat_image(item['id'], item['url'], item['width'], item['height'])

    # Création de l'application principale
    app = MainApplication(root, db=db)
    app.pack(expand=True, fill="both")

    # Lancement de l'interface utilisateur
    root.mainloop()

    # Fermer la connexion à la base de données
    db.close()

if __name__ == '__main__':
    main()
