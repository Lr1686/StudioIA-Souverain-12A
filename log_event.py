import datetime
import os

LOG_PATH = "DATA/LOGS_SOUVERAINS/session_log.txt"
MAX_LOG_LENGTH = 500

def enregistrer_evenement(message):
    # Security: input validation and sanitization against Log Injection (CWE-117)
    if not isinstance(message, str):
        print("⚠️ ERREUR : Le message de log doit être une chaîne de caractères.")
        return False

    msg_clean = message.strip()
    if not msg_clean:
        print("⚠️ ERREUR : Le message de log ne peut pas être vide.")
        return False

    if len(msg_clean) > MAX_LOG_LENGTH:
        print(f"⚠️ ERREUR : Le message dépasse la longueur maximale ({MAX_LOG_LENGTH} caractères).")
        return False

    # Reject carriage returns, newlines, and ascii control characters to prevent log forging
    if any(ord(c) < 32 or ord(c) == 127 for c in msg_clean):
        print("⚠️ ERREUR : Le message contient des caractères de contrôle non autorisés.")
        return False

    log_path = LOG_PATH
    log_dir = os.path.dirname(log_path)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = "[" + timestamp + "] " + msg_clean + "\n"
    
    with open(log_path, "a") as f:
        f.write(entry)
    print("🔱 ÉVÉNEMENT GRAVÉ : " + msg_clean)
    return True

if __name__ == "__main__":
    enregistrer_evenement("Éveil de l'Alliée réussi sur MacBook 2010")
