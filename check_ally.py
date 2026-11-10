import json
import os

CONFIG_PATH = "DATA/config_anastasia.json"


def initialiser_alliee():
    if not os.path.exists(CONFIG_PATH):
        print(
            f"⚠️ ERREUR : Le noyau d'identité est manquant (attendu : '{CONFIG_PATH}')."
        )
        print(
            "💡 CONSEIL : Vérifiez l'existence du fichier de configuration ou régénérez l'identité souveraine."
        )
        return False

    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(
            f"⚠️ ERREUR : Le fichier de configuration '{CONFIG_PATH}' est corrompu ou illisible."
        )
        print("💡 CONSEIL : Vérifiez la syntaxe JSON du fichier d'identité souveraine.")
        return False

    print("--- [ INITIALISATION ALLIÉE ] ---")
    print("ALIAS      : " + str(data.get("alias", "Non défini")))
    print("STATUT     : " + str(data.get("statut", "Non défini")))
    print("FRÉQUENCE  : " + str(data.get("frequence", "Non défini")))
    print("---")
    print("Souveraineté confirmée via " + str(data.get("origine", "Non défini")))
    return True


if __name__ == "__main__":
    initialiser_alliee()
