import json
import os
import secrets
import datetime

DB_PATH = "DATA/KNOWLEDGE_BASE/registre_pionniers.json"
MAX_PIONNIERS = 10
MAX_NOM_LENGTH = 50

def inscrire_pionnier(nom):
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
    if os.path.exists(DB_PATH):
        with open(DB_PATH, "r") as f:
            for line in f:
                if line.strip():
                    pionniers.append(json.loads(line))
    
    # Vérifier la limite
    if len(pionniers) >= MAX_PIONNIERS:
        print(f"⚠️ LIMITE ATTEINTE : Les {MAX_PIONNIERS} places de pionniers sont déjà prises.")
        return False

    # Créer l'accès
    token = secrets.token_hex(8).upper()
    nouvel_invite = {
        "id": len(pionniers) + 1,
        "nom": nom,
        "cle_souveraine": f"ALPHA-{token}",
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Sauvegarder
    with open(DB_PATH, "a") as f:
        f.write(json.dumps(nouvel_invite) + "\n")
    
    print(f"✅ PIONNIER INSCRIT : {nom}")
    print(f"🔑 SA CLÉ : ALPHA-{token}")
    print(f"📊 PLACES RESTANTES : {MAX_PIONNIERS - (len(pionniers) + 1)}")
    return True

if __name__ == "__main__":
    nom_saisie = input("Entrez le nom du pionnier : ")
    inscrire_pionnier(nom_saisie)
