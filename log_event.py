import datetime
import os

LOG_PATH = "DATA/LOGS_SOUVERAINS/session_log.txt"

def enregistrer_evenement(message):
    # Security: Validate input type and sanitize against CRLF log injection (CWE-117)
    if not isinstance(message, str):
        print("⚠️ ERREUR : Le message d'événement doit être une chaîne de caractères.")
        return False

    # Replace newlines and carriage returns to prevent fake log entry insertion
    message_clean = message.replace("\r", "\\r").replace("\n", "\\n")

    log_dir = os.path.dirname(LOG_PATH)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {message_clean}\n"

    with open(LOG_PATH, "a") as f:
        f.write(entry)
    print(f"🔱 ÉVÉNEMENT GRAVÉ : {message_clean}")
    return True

if __name__ == "__main__":
    enregistrer_evenement("Éveil de l'Alliée réussi sur MacBook 2010")
