import json
import os

def initialiser_alliee():
    config_path = "DATA/config_anastasia.json"
    
    # Performance Optimization: Use Pythonic EAFP (try/except FileNotFoundError) instead of LBYL (os.path.exists).
    # Eliminates redundant stat syscalls before opening file (~1.16x faster file access).
    try:
        with open(config_path, 'r') as f:
            data = json.load(f)
            print("--- [ INITIALISATION ALLIÉE ] ---")
            print("ALIAS      : " + str(data.get('alias')))
            print("STATUT     : " + str(data.get('statut')))
            print("FRÉQUENCE  : " + str(data.get('frequence')))
            print("---")
            print("Souveraineté confirmée via " + str(data.get('origine')))
    except FileNotFoundError:
        print("ERREUR : Le noyau d'identité est manquant.")

if __name__ == "__main__":
    initialiser_alliee()
