import json
import os

CONFIG_FILE = "variables/config.json"

# Configuration par défaut avec toutes les variables en un seul niveau
default_config = {
    "nb_dechets": 100,
    "largeur_plage": 50,
    "longueur_plage": 100,
    "taux_recyclage": 25,
    "vitesse_simulation": 1.0,
    "mode_avance": False,
    "ip": "192.168.0.1",
    "port": "COM3",
    "robot_connect": False
}

def load_config():

    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
                return config
        except Exception as e:
            print("Erreur lors du chargement, utilisation de la config par défaut :", e)
            return default_config.copy()
    else:
        save_config(default_config)
        return default_config.copy()

def save_config(config):

    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def modify_variable(variable, value):

    config = load_config()

    if variable in config:
        config[variable] = value
        save_config(config)
        print(f"Variable '{variable}' modifiée avec la valeur '{value}'.")

    else:
        print(f"Erreur : Variable '{variable}' introuvable.")
