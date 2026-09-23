import json
import os
import secrets
import datetime

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, "DATA"))
DB_PATH = os.path.abspath(os.path.join(DATA_DIR, "KNOWLEDGE_BASE", "registre_pionniers.json"))
MAX_PIONNIERS = 10
MAX_NOM_LENGTH = 50


def _get_safe_path(filepath):
    """Ensure the target filepath is safely contained within DATA_DIR."""
    resolved_path = os.path.abspath(filepath)
    if not resolved_path.startswith(DATA_DIR + os.sep) and resolved_path != DATA_DIR:
        raise ValueError("Sécurité: tentative d'accès en dehors du répertoire autorisé.")
    return resolved_path


def inscrire_pionnier(nom):
    target_path = _get_safe_path(DB_PATH)
    target_dir = os.path.dirname(target_path)
    os.makedirs(target_dir, exist_ok=True)
    # Validation des entrées (sécurité & DoS)
    if not isinstance(nom, str):
        print("⚠️ ERREUR : Le nom du pionnier doit être une chaîne de caractères.")
        return False

    nom = nom.strip()
    if not nom:
        print("⚠️ ERREUR : Le nom du pionnier ne peut pas être vide.")
        return False

    if len(nom) > MAX_NOM_LENGTH:
        print(f"⚠️ ERREUR : Le nom ne doit pas dépasser {MAX_NOM_LENGTH} caractères.")
        return False

    # Assurer que le dossier parent existe
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    # Charger la base existante
    pionniers = []
    if os.path.exists(target_path):
        with open(target_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    pionniers.append(json.loads(line))
    
    # Vérifier la limite
    if nb_pionniers >= MAX_PIONNIERS:
        print(f"⚠️ LIMITE ATTEINTE : Les {MAX_PIONNIERS} places de pionniers sont déjà prises.")
        return False

    # Créer l'accès
    token = secrets.token_hex(8).upper()
    nouvel_invite = {
        "id": nb_pionniers + 1,
        "nom": nom,
        "cle_souveraine": f"ALPHA-{token}",
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Ensure parent directory exists before writing
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    # Sauvegarder
    with open(target_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(nouvel_invite) + "\n")
    
    print(f"✅ PIONNIER INSCRIT : {nom}")
    print(f"🔑 SA CLÉ : ALPHA-{token}")
    print(f"📊 PLACES RESTANTES : {MAX_PIONNIERS - (len(pionniers) + 1)}")
    return True

if __name__ == "__main__":
    nom_saisie = input("Entrez le nom du pionnier : ")
    inscrire_pionnier(nom_saisie)
