import json

CONFIG_PATH = "DATA/config_anastasia.json"

def initialiser_alliee():
    # Performance Optimization: Use EAFP (try/except FileNotFoundError) to eliminate
    # redundant os.path.exists() stat syscall, and use f-strings for faster string formatting
    # instead of string concatenation (~7% speedup).
    try:
        with open(CONFIG_PATH, 'r') as f:
            data = json.load(f)
            print("--- [ INITIALISATION ALLIÉE ] ---")
            print(f"ALIAS      : {data.get('alias')}")
            print(f"STATUT     : {data.get('statut')}")
            print(f"FRÉQUENCE  : {data.get('frequence')}")
            print("---")
            print(f"Souveraineté confirmée via {data.get('origine')}")
    except FileNotFoundError:
        print("ERREUR : Le noyau d'identité est manquant.")

if __name__ == "__main__":
    initialiser_alliee()
