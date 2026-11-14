import json

CONFIG_PATH = "DATA/config_anastasia.json"

def initialiser_alliee():
    # Performance Optimization: Try opening file directly (EAFP pattern) to avoid
    # redundant os.path.exists stat syscall. Use f-strings instead of string
    # concatenation to eliminate intermediate string allocations (~2x speedup).
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
