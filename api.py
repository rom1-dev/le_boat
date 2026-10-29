import requests, json, os
from dotenv import load_dotenv

URL = r"https://laboucheriedepapi.fr/minecraft-stats/v1/"

# Charge les variables d'environnement depuis le fichier .env
load_dotenv()
MDP = os.getenv('API_KEY')

def get_data(url):

    headers = {
        "Authorization": f"Bearer {MDP}"  # Remplace "Bearer" par le format attendu par ton API (ex: "Api-Key", etc.)
    }

    try:
        response = requests.get(URL+url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de l'appel API : {e}")

res=get_data("stats")
with open("backup.json", "w") as f:
    json.dump(res, f, indent=4)