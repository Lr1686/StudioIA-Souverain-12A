import datetime
import os

LOG_PATH = "DATA/LOGS_SOUVERAINS/session_log.txt"


def enregistrer_evenement(message):
    # Security: Input validation to ensure message is a string
    if not isinstance(message, str):
        message = str(message)

    # Security (CWE-117): Sanitize newlines and control characters to prevent log injection
    clean_message = "".join(
        c if ord(c) >= 32 and ord(c) != 127 else " " for c in message
    ).strip()

    if not clean_message:
        clean_message = "[EMPTY_MESSAGE]"

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {clean_message}\n"

    # Ensure log directory exists
    log_dir = os.path.dirname(LOG_PATH)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    with open(LOG_PATH, "a") as f:
        f.write(entry)
    print("🔱 ÉVÉNEMENT GRAVÉ : " + clean_message)


if __name__ == "__main__":
    enregistrer_evenement("Éveil de l'Alliée réussi sur MacBook 2010")
