import datetime
import json
import os

LOG_PATH = "DATA/LOGS_SOUVERAINS/session_log.txt"

def enregistrer_evenement(message):
    # Input validation: check type
    if not isinstance(message, str):
        print("⚠️ ERREUR : Le message doit être une chaîne de caractères.")
        return False

    message_clean = message.strip()
    if not message_clean:
        print("⚠️ ERREUR : Le message de log ne peut pas être vide.")
        return False

    # Prevent CRLF / log injection by sanitizing newlines and carriage returns
    message_clean = message_clean.replace("\r", " ").replace("\n", " ")

    # Ensure log directory exists
    log_dir = os.path.dirname(LOG_PATH)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {message_clean}\n"
    
    with open(LOG_PATH, "a") as f:
        f.write(entry)
    print("🔱 ÉVÉNEMENT GRAVÉ : " + message_clean)
    return True

if __name__ == "__main__":
    enregistrer_evenement("Éveil de l'Alliée réussi sur MacBook 2010")
