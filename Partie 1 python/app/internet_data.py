import requests

class InternetDataFetcher:
    def __init__(self, url):
        self.url = url

    def fetch_json(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()  # Vérification de la requête
            return response.json()      
        except requests.exceptions.HTTPError as e:
            print(f"Erreur HTTP: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Erreur de requête: {e}")
