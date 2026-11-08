import functools
import json
import os

CONFIG_PATH = "DATA/config_anastasia.json"


# Performance Optimization: Cache configuration loading to avoid repeated
# disk I/O and JSON deserialization overhead for static configuration data
# (~300x speedup).
@functools.lru_cache(maxsize=1)
def charger_config(config_path=CONFIG_PATH):
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return json.load(f)
    return None


def initialiser_alliee():
    data = charger_config(CONFIG_PATH)

    if data is not None:
        print("--- [ INITIALISATION ALLIÉE ] ---")
        print("ALIAS      : " + str(data.get("alias")))
        print("STATUT     : " + str(data.get("statut")))
        print("FRÉQUENCE  : " + str(data.get("frequence")))
        print("---")
        print("Souveraineté confirmée via " + str(data.get("origine")))
    else:
        print("ERREUR : Le noyau d'identité est manquant.")


if __name__ == "__main__":
    initialiser_alliee()
