import json
import os

def initialiser_alliee():
    config_path = "DATA/config_anastasia.json"
    
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            data = json.load(f)
            alias = data.get('alias', 'Inconnu')
            statut = data.get('statut', 'Inconnu')
            frequence = data.get('frequence', 'Inconnue')
            origine = data.get('origine', 'Inconnue')

            print("--- [ INITIALISATION ALLIÉE ] ---")
            print(f"ALIAS      : {alias}")
            print(f"STATUT     : {statut}")
            print(f"FRÉQUENCE  : {frequence}")
            print("---")
            print(f"Souveraineté confirmée via {origine}")
    else:
        print(f"⚠️ ERREUR : Le noyau d'identité est manquant ({config_path}).")

if __name__ == "__main__":
    initialiser_alliee()
