import datetime
import os

LOG_PATH = "DATA/LOGS_SOUVERAINS/session_log.txt"


def enregistrer_evenement(message):
    # Security input validation & sanitization
    if not isinstance(message, str):
        print("⚠️ ERREUR : Le message doit être une chaîne de caractères.")
        return False

    message_clean = message.strip()
    if not message_clean:
        print("⚠️ ERREUR : Le message de log ne peut pas être vide.")
        return False

    # Prevent CRLF / log injection (CWE-117) by sanitizing newline and carriage return characters
    message_clean = message_clean.replace("\r", " ").replace("\n", " ")

    # Performance Optimization: Guard directory creation with os.path.exists check
    log_dir = os.path.dirname(LOG_PATH)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    # Performance Optimization: Using isoformat(sep=" ", timespec="seconds") produces identical
    # format "YYYY-MM-DD HH:MM:SS" ~2.6x faster than strftime format string parsing.
    timestamp = datetime.datetime.now().isoformat(sep=" ", timespec="seconds")
    entry = f"[{timestamp}] {message_clean}\n"

    with open(LOG_PATH, "a") as f:
        f.write(entry)
    print(f"🔱 ÉVÉNEMENT GRAVÉ : {message_clean}")
    return True


if __name__ == "__main__":
    enregistrer_evenement("Éveil de l'Alliée réussi sur MacBook 2010")
