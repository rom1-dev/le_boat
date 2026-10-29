import json
import os
import requests
from dotenv import load_dotenv

# Charge les variables d'environnement depuis le fichier .env
load_dotenv()
URL = r"https://laboucheriedepapi.fr/minecraft-stats/v1/"
MDP = os.getenv('API_KEY')

# Chargement dynamique des unités depuis le fichier stats_units.json
try:
    with open('stats_units.json', 'r', encoding='utf-8') as f:
        MINECRAFT_STATS_UNITS = json.load(f)
except FileNotFoundError:
    print("Attention : Le fichier stats_units.json est introuvable.")
    MINECRAFT_STATS_UNITS = {}

def get_data(endpoint):
    headers = {
        "Authorization": f"Bearer {MDP}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(URL + endpoint, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de l'appel API : {e}")
        return None

def convert_stat_value(stat_key, raw_value):
    """Applique le calcul de conversion selon l'unité chargée depuis le JSON."""
    unit = MINECRAFT_STATS_UNITS.get(stat_key, "")
    
    try:
        val = float(raw_value)
    except (ValueError, TypeError):
        return raw_value

    if unit == "heures":
        return round(val / (3600 * 20), 1)
    elif unit == "km":
        return round(val / 100000, 2)
    elif unit == "cœurs":
        return round((val / 20) * 2) / 2
        
    return raw_value

def get_player_stat(player_identifier, category, stat):
    """
    Récupère une statistique précise via l'endpoint ciblé (ex: players/Isotope235/custom/play_time).
    """
    # Nettoyage des préfixes éventuels pour l'endpoint et le dictionnaire d'unités
    clean_category = category.replace("minecraft:", "")
    clean_stat = stat.replace("minecraft:", "")
    
    # Construction de l'endpoint précis
    endpoint = f"players/{player_identifier}/{clean_category}/{clean_stat}"
    
    data = get_data(endpoint)
    if not data or "value" not in data:
        return None, ""

    raw_value = data["value"]

    # Si c'est la catégorie custom, on récupère l'unité du JSON et on convertit
    final_value = raw_value
    unit = ""
    if clean_category.lower() == "custom":
        unit = MINECRAFT_STATS_UNITS.get(clean_stat, "")
        final_value = convert_stat_value(clean_stat, raw_value)

    return final_value, unit

def formater_nombre(nombre):
    try:
        if isinstance(nombre, float):
            return f"{nombre}".replace(".", ",")
        return f"{int(nombre):,}".replace(",", " ")
    except (ValueError, TypeError):
        return nombre

def get_stats_ranking(category, stat, limit=3, order="desc", ignore_bots=True, ignore_unknown=True):
    """
    Récupère un classement pour une statistique spécifique, avec conversion des unités et filtres activés par défaut.
    """
    clean_category = category.replace("minecraft:", "")
    clean_stat = stat.replace("minecraft:", "")
    
    endpoint = f"stats/{clean_category}/{clean_stat}?limit={limit}&order={order}&ignoreBots={str(ignore_bots).lower()}&ignoreUnknown={str(ignore_unknown).lower()}"
    
    data = get_data(endpoint)
    if not data or "players" not in data:
        return None, ""

    unit = ""
    if clean_category.lower() == "custom":
        unit = MINECRAFT_STATS_UNITS.get(clean_stat, "")
        # Application de la conversion d'unité sur chaque joueur du classement
        for player in data["players"]:
            if "value" in player:
                player["value"] = convert_stat_value(clean_stat, player["value"])

    return data["players"], unit