import json
import os

CONFIG_PATH = "DATA/config_anastasia.json"


def initialiser_alliee():
    if not os.path.exists(CONFIG_PATH):
        print(
            f"⚠️ ERREUR : Le noyau d'identité est manquant ({CONFIG_PATH} non trouvé)."
        )
        return False

    with open(CONFIG_PATH, "r") as f:
        data = json.load(f)

    alias = data.get("alias", "Inconnu")
    statut = data.get("statut", "Inconnu")
    frequence = data.get("frequence", "Non assignée")
    origine = data.get("origine", "Origine indéterminée")

    print("--- [ INITIALISATION ALLIÉE ] ---")
    print(f"ALIAS      : {alias}")
    print(f"STATUT     : {statut}")
    print(f"FRÉQUENCE  : {frequence}")
    print("---")
    print(f"✅ Souveraineté confirmée via {origine}")
    return True


if __name__ == "__main__":
    initialiser_alliee()
