import datetime
import os

LOG_PATH = "DATA/LOGS_SOUVERAINS/session_log.txt"
MAX_LOG_LENGTH = 500

def enregistrer_evenement(message):
    """Enregistre un événement dans les logs de manière sécurisée (prévention d'injection de logs)."""
    if not isinstance(message, str):
        print("⚠️ ERREUR LOG : Le message doit être une chaîne de caractères.")
        return False

    # Sanitization contre l'injection de log (Log Injection / CRLF Injection)
    # Remplacer les saut de ligne (\n, \r) et caractères de contrôle / null bytes par un espace ou underscore
    cleaned_message = message.replace("\r", " ").replace("\n", " ").replace("\0", "")
    # Enlever tout autre caractère de contrôle ASCII
    cleaned_message = "".join(c for c in cleaned_message if ord(c) >= 32 or ord(c) > 127).strip()

    if not cleaned_message:
        print("⚠️ ERREUR LOG : Le message est vide ou invalide.")
        return False

    if len(cleaned_message) > MAX_LOG_LENGTH:
        cleaned_message = cleaned_message[:MAX_LOG_LENGTH] + "... [TRONQUÉ]"

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {cleaned_message}\n"

    parent_dir = os.path.dirname(LOG_PATH)
    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)

    with open(LOG_PATH, "a") as f:
        f.write(entry)
    print("🔱 ÉVÉNEMENT GRAVÉ : " + cleaned_message)
    return True

if __name__ == "__main__":
    enregistrer_evenement("Éveil de l'Alliée réussi sur MacBook 2010")
