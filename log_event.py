import datetime
import os

LOG_PATH = "DATA/LOGS_SOUVERAINS/session_log.txt"
MAX_MESSAGE_LENGTH = 500

def enregistrer_evenement(message):
    # Security input validation & sanitization to prevent log injection / forgery
    if not isinstance(message, str):
        print("⚠️ ERREUR : Le message doit être une chaîne de caractères.")
        return False

    msg_clean = message.strip()
    if not msg_clean:
        print("⚠️ ERREUR : Le message d'événement ne peut pas être vide.")
        return False

    if len(msg_clean) > MAX_MESSAGE_LENGTH:
        print(f"⚠️ ERREUR : Le message dépasse la longueur maximale autorisée ({MAX_MESSAGE_LENGTH} caractères).")
        return False

    # Disallow newlines and ASCII control characters to prevent log forging
    if any(ord(c) < 32 or ord(c) == 127 for c in msg_clean):
        print("⚠️ ERREUR : Le message contient des caractères non autorisés.")
        return False

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {msg_clean}\n"

    parent_dir = os.path.dirname(LOG_PATH)
    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)

    with open(LOG_PATH, "a") as f:
        f.write(entry)
    print(f"🔱 ÉVÉNEMENT GRAVÉ : {msg_clean}")
    return True

if __name__ == "__main__":
    enregistrer_evenement("Éveil de l'Alliée réussi sur MacBook 2010")
