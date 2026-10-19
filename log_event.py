import datetime
import os

LOG_PATH = "DATA/LOGS_SOUVERAINS/session_log.txt"
MAX_LOG_LENGTH = 500

def enregistrer_evenement(message):
    # Validation inputs to prevent log injection / log forgery
    if not isinstance(message, str):
        print("⚠️ ERREUR : Le message de log doit être une chaîne de caractères.")
        return False

    message_clean = message.strip()
    if not message_clean:
        print("⚠️ ERREUR : Le message de log ne peut pas être vide.")
        return False

    if len(message_clean) > MAX_LOG_LENGTH:
        print(f"⚠️ ERREUR : Le message de log dépasse la longueur maximale ({MAX_LOG_LENGTH} caractères).")
        return False

    # Prevent CRLF / newline log injection and unprintable control characters
    if any(ord(c) < 32 or ord(c) == 127 for c in message_clean):
        print("⚠️ ERREUR : Le message de log contient des caractères non autorisés (caractères de contrôle/sauts de ligne).")
        return False

    parent_dir = os.path.dirname(LOG_PATH)
    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {message_clean}\n"
    
    with open(LOG_PATH, "a") as f:
        f.write(entry)
    print("🔱 ÉVÉNEMENT GRAVÉ : " + message_clean)
    return True

if __name__ == "__main__":
    enregistrer_evenement("Éveil de l'Alliée réussi sur MacBook 2010")
