import datetime
import os

LOG_PATH = "DATA/LOGS_SOUVERAINS/session_log.txt"
MAX_MESSAGE_LENGTH = 1000

def enregistrer_evenement(message):
    """Enregistre un événement dans les logs de manière sécurisée (prévention CWE-117)."""
    if not isinstance(message, str):
        print("⚠️ ERREUR : Le message de log doit être une chaîne de caractères.")
        return False

    clean_message = message.strip()
    if not clean_message:
        print("⚠️ ERREUR : Le message de log ne peut pas être vide.")
        return False

    if len(clean_message) > MAX_MESSAGE_LENGTH:
        print(f"⚠️ ERREUR : Le message dépasse la longueur maximale ({MAX_MESSAGE_LENGTH} caractères).")
        return False

    # Protection contre l'injection de logs (CWE-117) :
    # Remplace les retours à la ligne et caractères de contrôle par un espace
    sanitized_message = "".join(
        c if (ord(c) >= 32 and ord(c) != 127) or ord(c) > 159 else " "
        for c in clean_message
    )

    parent_dir = os.path.dirname(LOG_PATH)
    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {sanitized_message}\n"

    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(entry)

    print(f"🔱 ÉVÉNEMENT GRAVÉ : {sanitized_message}")
    return True

if __name__ == "__main__":
    enregistrer_evenement("Éveil de l'Alliée réussi sur MacBook 2010")
