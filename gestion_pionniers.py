import datetime
import json
import os
import secrets

DB_PATH = "DATA/KNOWLEDGE_BASE/registre_pionniers.json"
MAX_PIONNIERS = 10

MAX_NOM_LENGTH = 100


def compter_pionniers():
    if os.path.exists(DB_PATH):
        with open(DB_PATH, "r") as f:
            return sum(1 for line in f if line.strip())
    return 0


def inscrire_pionnier(nom):
    # Security input validation & sanitization
    if not isinstance(nom, str):
        print("⚠️ ERREUR : Le nom doit être une chaîne de caractères.")
        return False

    nom_clean = nom.strip()
    if not nom_clean:
        print("⚠️ ERREUR : Le nom du pionnier ne peut pas être vide.")
        return False

    if len(nom_clean) > MAX_NOM_LENGTH:
        print(
            f"⚠️ ERREUR : Le nom dépasse la longueur maximale autorisée ({MAX_NOM_LENGTH} caractères)."
        )
        return False

    if any(ord(c) < 32 or ord(c) == 127 for c in nom_clean):
        print("⚠️ ERREUR : Le nom contient des caractères non autorisés.")
        return False

    nom = nom_clean

    nb_pionniers = compter_pionniers()

    # Vérifier la limite
    if nb_pionniers >= MAX_PIONNIERS:
        print(
            f"⚠️ LIMITE ATTEINTE : Les {MAX_PIONNIERS} places de pionniers sont déjà prises."
        )
        return False

    # Créer l'accès
    token = secrets.token_hex(8).upper()
    nouvel_invite = {
        "id": nb_pionniers + 1,
        "nom": nom,
        "cle_souveraine": f"ALPHA-{token}",
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    parent_dir = os.path.dirname(DB_PATH)
    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)

    # Sauvegarder
    with open(DB_PATH, "a") as f:
        f.write(json.dumps(nouvel_invite) + "\n")

    print(f"✅ PIONNIER INSCRIT : {nom}")
    print(f"🔑 SA CLÉ : ALPHA-{token}")
    print(f"📊 PLACES RESTANTES : {MAX_PIONNIERS - (nb_pionniers + 1)}")
    return True


if __name__ == "__main__":
    nb = compter_pionniers()
    places_restantes = MAX_PIONNIERS - nb
    print("--- [ GESTION DES PIONNIERS ] ---")
    if places_restantes <= 0:
        print(
            f"⚠️ LIMITE ATTEINTE : Les {MAX_PIONNIERS} places de pionniers sont déjà prises."
        )
    else:
        print(f"📊 PLACES RESTANTES : {places_restantes}/{MAX_PIONNIERS}")
        nom_saisie = input("👉 Entrez le nom du pionnier : ")
        inscrire_pionnier(nom_saisie)
