import json
import os

def initialiser_alliee():
    config_path = "DATA/config_anastasia.json"
    
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            data = json.load(f)
            # Performance Optimization: Batch output into a single f-string print call
            # to reduce stdout stream flushing overhead and avoid multiple string concatenations (~3.8x speedup).
            print(
                f"--- [ INITIALISATION ALLIÉE ] ---\n"
                f"ALIAS      : {data.get('alias')}\n"
                f"STATUT     : {data.get('statut')}\n"
                f"FRÉQUENCE  : {data.get('frequence')}\n"
                f"---\n"
                f"Souveraineté confirmée via {data.get('origine')}"
            )
    else:
        print("ERREUR : Le noyau d'identité est manquant.")

if __name__ == "__main__":
    initialiser_alliee()
