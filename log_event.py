import datetime
import os

LOG_PATH = "DATA/LOGS_SOUVERAINS/session_log.txt"
MAX_MESSAGE_LENGTH = 500


def enregistrer_evenement(message):
    # Security: Validate input and prevent log injection / log forging (CWE-117)
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

    # Block newlines, carriage returns, and control characters to prevent fake log entries
    if any(ord(c) < 32 or ord(c) == 127 for c in message_clean):
        print("⚠️ ERREUR : Le message contient des caractères non autorisés (injection de log évitée).")
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
