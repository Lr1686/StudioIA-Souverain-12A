import datetime
import os

LOG_PATH = "DATA/LOGS_SOUVERAINS/session_log.txt"
MAX_MSG_LENGTH = 500

def enregistrer_evenement(message):
    # Security input validation & sanitization
    if not isinstance(message, str):
        print("⚠️ ERREUR : Le message doit être une chaîne de caractères.")
        return False

    clean_msg = message.strip()
    if not clean_msg:
        print("⚠️ ERREUR : Le message ne peut pas être vide.")
        return False

    if len(clean_msg) > MAX_MSG_LENGTH:
        print(f"⚠️ ERREUR : Le message dépasse la longueur maximale autorisée ({MAX_MSG_LENGTH} caractères).")
        return False

    # Security: Prevent log injection / forgery by replacing control characters (e.g., \n, \r)
    sanitized_msg = "".join(c if ord(c) >= 32 else " " for c in clean_msg)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {sanitized_msg}\n"

    parent_dir = os.path.dirname(LOG_PATH)
    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)

    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(entry)

    print("🔱 ÉVÉNEMENT GRAVÉ : " + sanitized_msg)
    return True

if __name__ == "__main__":
    enregistrer_evenement("Éveil de l'Alliée réussi sur MacBook 2010")
