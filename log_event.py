import datetime
import os

LOG_PATH = "DATA/LOGS_SOUVERAINS/session_log.txt"
MAX_LOG_LENGTH = 500

def enregistrer_evenement(message):
    # Security input validation & sanitization (prevents log injection)
    if not isinstance(message, str):
        print("⚠️ ERREUR : Le message doit être une chaîne de caractères.")
        return False

    msg_clean = message.strip()
    if not msg_clean:
        print("⚠️ ERREUR : Le message ne peut pas être vide.")
        return False

    if len(msg_clean) > MAX_LOG_LENGTH:
        print(f"⚠️ ERREUR : Le message dépasse la longueur maximale autorisée ({MAX_LOG_LENGTH} caractères).")
        return False

    if any(ord(c) < 32 or ord(c) == 127 for c in msg_clean):
        print("⚠️ ERREUR : Le message contient des caractères non autorisés.")
        return False

    log_dir = os.path.dirname(LOG_PATH)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {msg_clean}\n"
    
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(entry)
    print("🔱 ÉVÉNEMENT GRAVÉ : " + msg_clean)
    return True

if __name__ == "__main__":
    enregistrer_evenement("Éveil de l'Alliée réussi sur MacBook 2010")
