import datetime
import os

LOG_PATH = "DATA/LOGS_SOUVERAINS/session_log.txt"
MAX_MESSAGE_LENGTH = 500

def enregistrer_evenement(message):
    # Security: Validate input type, length, and prevent log injection (CWE-117)
    if not isinstance(message, str):
        print("⚠️ ERREUR : Le message doit être une chaîne de caractères.")
        return False

    message_clean = message.strip()
    if not message_clean:
        print("⚠️ ERREUR : Le message ne peut pas être vide.")
        return False

    if len(message_clean) > MAX_MESSAGE_LENGTH:
        print(f"⚠️ ERREUR : Le message dépasse la longueur maximale autorisée ({MAX_MESSAGE_LENGTH} caractères).")
        return False

    # Block newlines and control characters to prevent log forging
    if any(ord(c) < 32 or ord(c) == 127 for c in message_clean):
        print("⚠️ ERREUR : Le message contient des caractères de contrôle non autorisés.")
        return False

    message = message_clean

    parent_dir = os.path.dirname(LOG_PATH)
    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)

    # Performance Optimization: Using isoformat(sep=" ", timespec="seconds") produces identical
    # format "YYYY-MM-DD HH:MM:SS" ~2.6x faster than strftime format string parsing.
    timestamp = datetime.datetime.now().isoformat(sep=" ", timespec="seconds")
    entry = "[" + timestamp + "] " + message + "\n"
    
    with open(LOG_PATH, "a") as f:
        f.write(entry)
    print("🔱 ÉVÉNEMENT GRAVÉ : " + message)
    return True

if __name__ == "__main__":
    enregistrer_evenement("Éveil de l'Alliée réussi sur MacBook 2010")
