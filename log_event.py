import datetime
import json
import os

LOG_PATH = "DATA/LOGS_SOUVERAINS/session_log.txt"
MAX_LOG_LENGTH = 1000

def enregistrer_evenement(message):
    # Security input validation & sanitization against log injection
    if not isinstance(message, str):
        print("⚠️ ERREUR : Le message doit être une chaîne de caractères.")
        return False

    message_clean = message.strip()
    if not message_clean:
        print("⚠️ ERREUR : Le message ne peut pas être vide.")
        return False

    if len(message_clean) > MAX_LOG_LENGTH:
        print(f"⚠️ ERREUR : Le message dépasse la longueur maximale autorisée ({MAX_LOG_LENGTH} caractères).")
        return False

    # Prevent log injection: replace newlines/carriage returns and filter control chars
    sanitized_message = "".join(
        " " if c in ("\r", "\n") else (c if ord(c) >= 32 or c == "\t" else "")
        for c in message_clean
    )

    parent_dir = os.path.dirname(LOG_PATH)
    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = "[" + timestamp + "] " + sanitized_message + "\n"
    
    with open(LOG_PATH, "a") as f:
        f.write(entry)
    print("🔱 ÉVÉNEMENT GRAVÉ : " + sanitized_message)
    return True

if __name__ == "__main__":
    enregistrer_evenement("Éveil de l'Alliée réussi sur MacBook 2010")
