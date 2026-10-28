import datetime
import os

LOG_PATH = "DATA/LOGS_SOUVERAINS/session_log.txt"


def enregistrer_evenement(message):
    # Input validation: check type
    if not isinstance(message, str):
        print("⚠️ ERREUR : Le message doit être une chaîne de caractères.")
        return False

    # Security input sanitization (prevent log injection CWE-117)
    # Strip leading/trailing whitespaces and replace control chars & newlines
    clean_message = "".join(
        c if (ord(c) >= 32 or c == "\t") and c not in "\r\n" else " "
        for c in message
    ).strip()
    if not clean_message:
        print("⚠️ ERREUR : Le message de l'événement ne peut pas être vide.")
        return False

    parent_dir = os.path.dirname(LOG_PATH)
    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {clean_message}\n"

    with open(LOG_PATH, "a") as f:
        f.write(entry)
    print("🔱 ÉVÉNEMENT GRAVÉ : " + clean_message)
    return True


if __name__ == "__main__":
    enregistrer_evenement("Éveil de l'Alliée réussi sur MacBook 2010")
