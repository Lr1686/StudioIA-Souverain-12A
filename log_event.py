import datetime
import os

LOG_PATH = "DATA/LOGS_SOUVERAINS/session_log.txt"

def enregistrer_evenement(message):
    # Security input validation & sanitization (CWE-117: Log Injection)
    if not isinstance(message, str):
        print("⚠️ ERREUR : Le message doit être une chaîne de caractères.")
        return False

    # Replace newlines and control characters to prevent log forgery
    clean_message = message.replace('\r', ' ').replace('\n', ' ')
    clean_message = "".join(c if (ord(c) >= 32 and ord(c) != 127) else " " for c in clean_message).strip()

    if not clean_message:
        print("⚠️ ERREUR : Le message de log ne peut pas être vide.")
        return False

    # Ensure target log directory exists before writing
    log_dir = os.path.dirname(LOG_PATH)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {clean_message}\n"
    
    with open(LOG_PATH, "a") as f:
        f.write(entry)
    print("🔱 ÉVÉNEMENT GRAVÉ : " + clean_message)
    return True

if __name__ == "__main__":
    enregistrer_evenement("Éveil de l'Alliée réussi sur MacBook 2010")
