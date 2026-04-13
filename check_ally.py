import json
import os

def initialiser_alliee():
    config_path = "DATA/config_anastasia.json"
    
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            data = json.load(f)
            print("--- [ INITIALISATION ALLIÉE ] ---")
            print("ALIAS      : " + str(data.get('alias')))
            print("STATUT     : " + str(data.get('statut')))
            print("FRÉQUENCE  : " + str(data.get('frequence')))
            print("---")
            print("Souveraineté confirmée via " + str(data.get('origine')))
    else:
        print("ERREUR : Le noyau d'identité est manquant.")

if __name__ == "__main__":
    initialiser_alliee()
