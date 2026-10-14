import datetime
import os

LOG_PATH = "DATA/LOGS_SOUVERAINS/session_log.txt"
MAX_LOG_LENGTH = 500

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
        message_clean = message_clean[:MAX_LOG_LENGTH]

    # Sanitize control characters and newlines to prevent log forging / CRLF injection
    message_clean = "".join(" " if ord(c) < 32 or ord(c) == 127 else c for c in message_clean)

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
