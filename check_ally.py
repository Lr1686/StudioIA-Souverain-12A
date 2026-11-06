import json
import os

CONFIG_PATH = "DATA/config_anastasia.json"


def initialiser_alliee():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            data = json.load(f)
            print("--- [ INITIALISATION ALLIÉE ] ---")
            print("ALIAS      : " + str(data.get("alias")))
            print("STATUT     : " + str(data.get("statut")))
            print("FRÉQUENCE  : " + str(data.get("frequence")))
            print("---")
            print("✅ Souveraineté confirmée via " + str(data.get("origine")))
        return True
    else:
        print(
            f"⚠️ ERREUR : Le noyau d'identité est manquant (fichier introuvable : '{CONFIG_PATH}')."
        )
        print(
            "💡 CONSEIL : Vérifiez que le fichier de configuration existe dans DATA/ avant d'initialiser l'alliée."
        )
        return False


if __name__ == "__main__":
    initialiser_alliee()
