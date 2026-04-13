import json
import os
import secrets
import datetime

DB_PATH = "DATA/KNOWLEDGE_BASE/registre_pionniers.json"
MAX_PIONNIERS = 10

def inscrire_pionnier(nom):
    # Charger la base existante
    pionniers = []
    if os.path.exists(DB_PATH):
        with open(DB_PATH, "r") as f:
            for line in f:
                pionniers.append(json.loads(line))
    
    # Vérifier la limite
    if len(pionniers) >= MAX_PIONNIERS:
        print(f"⚠️ LIMITE ATTEINTE : Les {MAX_PIONNIERS} places de pionniers sont déjà prises.")
        return

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

if __name__ == "__main__":
    nom_saisie = input("Entrez le nom du pionnier : ")
    inscrire_pionnier(nom_saisie)
