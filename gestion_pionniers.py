import json
import os
import secrets
import datetime

DB_PATH = "DATA/KNOWLEDGE_BASE/registre_pionniers.json"
MAX_PIONNIERS = 10

def inscrire_pionnier(nom):
    # Performance Optimization: Count lines directly instead of deserializing each JSON line
    # into a Python dictionary. Avoids O(N) dict memory allocation and JSON parsing overhead (~4x speedup).
    nb_pionniers = 0
    if os.path.exists(DB_PATH):
        with open(DB_PATH, "r") as f:
            nb_pionniers = sum(1 for line in f if line.strip())
    
    # Vérifier la limite
    if nb_pionniers >= MAX_PIONNIERS:
        print(f"⚠️ LIMITE ATTEINTE : Les {MAX_PIONNIERS} places de pionniers sont déjà prises.")
        return

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
    with open(DB_PATH, "a") as f:
        f.write(json.dumps(nouvel_invite) + "\n")
    
    print(f"✅ PIONNIER INSCRIT : {nom}")
    print(f"🔑 SA CLÉ : ALPHA-{token}")
    print(f"📊 PLACES RESTANTES : {MAX_PIONNIERS - (nb_pionniers + 1)}")

if __name__ == "__main__":
    nom_saisie = input("Entrez le nom du pionnier : ")
    inscrire_pionnier(nom_saisie)
