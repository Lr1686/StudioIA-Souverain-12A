import datetime
import os

LOG_PATH = "DATA/LOGS_SOUVERAINS/session_log.txt"

def enregistrer_evenement(message):
    """Enregistre un événement dans le journal de session.
    
    Security: Validates input and sanitizes newlines to prevent Log Injection (CWE-117).
    """
    if not isinstance(message, str):
        print("⚠️ ERREUR : Le message doit être une chaîne de caractères.")
        return False

    message_clean = message.strip()
    if not message_clean:
        print("⚠️ ERREUR : Le message ne peut pas être vide.")
        return False

    # Security: Replace newlines to prevent attackers from forging fake log entries (CWE-117)
    safe_message = message_clean.replace("\r", " ").replace("\n", " ")

    parent_dir = os.path.dirname(LOG_PATH)
    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {safe_message}\n"

    with open(LOG_PATH, "a") as f:
        f.write(entry)
    print(f"🔱 ÉVÉNEMENT GRAVÉ : {safe_message}")
    return True

if __name__ == "__main__":
    enregistrer_evenement("Éveil de l'Alliée réussi sur MacBook 2010")
