import datetime
import os

LOG_PATH = "DATA/LOGS_SOUVERAINS/session_log.txt"


def enregistrer_evenement(message):
    # Input validation
    if not isinstance(message, str):
        print("⚠️ ERREUR : Le message de log doit être une chaîne de caractères.")
        return False

    # Security (CWE-117 Log Injection Mitigation):
    # Sanitize newlines, carriage returns and control characters to prevent log forging
    clean_message = message.replace("\r", "\\r").replace("\n", "\\n")
    clean_message = "".join(
        c if ord(c) >= 32 or c == "\t" else f"\\x{ord(c):02x}"
        for c in clean_message
    )

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {clean_message}\n"

    parent_dir = os.path.dirname(LOG_PATH)
    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)

    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(entry)
    print("🔱 ÉVÉNEMENT GRAVÉ : " + clean_message)
    return True


if __name__ == "__main__":
    enregistrer_evenement("Éveil de l'Alliée réussi sur MacBook 2010")
