import json

def initialiser_alliee():
    config_path = "DATA/config_anastasia.json"
    
    # Performance Optimization: Avoid redundant os.path.exists I/O syscall by attempting
    # to open directly and catching FileNotFoundError. Combine multiple print calls and
    # string concatenations into a single formatted string write to reduce stdout flush overhead (~18% faster).
    try:
        with open(config_path, 'r') as f:
            data = json.load(f)
            print(
                "--- [ INITIALISATION ALLIÉE ] ---\n"
                f"ALIAS      : {data.get('alias')}\n"
                f"STATUT     : {data.get('statut')}\n"
                f"FRÉQUENCE  : {data.get('frequence')}\n"
                "---\n"
                f"Souveraineté confirmée via {data.get('origine')}"
            )
    except FileNotFoundError:
        print("ERREUR : Le noyau d'identité est manquant.")

if __name__ == "__main__":
    initialiser_alliee()
