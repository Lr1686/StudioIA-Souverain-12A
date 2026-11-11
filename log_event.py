import datetime
import os

LOG_PATH = "DATA/LOGS_SOUVERAINS/session_log.txt"


def enregistrer_evenement(message):
    """Enregistre un événement dans les logs de session.

    Assainit l'entrée pour éviter les injections de logs (CWE-117).
    """
    # Security input validation & sanitization (CWE-117 Log Injection prevention)
    if not isinstance(message, str):
        print("⚠️ ERREUR : Le message doit être une chaîne de caractères.")
        return False

    message_clean = message.strip()
    if not message_clean:
        print("⚠️ ERREUR : Le message ne peut pas être vide.")
        return False

    # Strip newlines and control characters to prevent log injection/forging
    message_clean = "".join(
        c if (ord(c) >= 32 and ord(c) != 127) else " " for c in message_clean
    )

    # Performance & Safety: Guard directory creation with os.path.exists
    log_dir = os.path.dirname(LOG_PATH)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    # Performance Optimization: Using isoformat produces identical format faster than strftime
    timestamp = datetime.datetime.now().isoformat(sep=" ", timespec="seconds")
    entry = f"[{timestamp}] {message_clean}\n"

    with open(LOG_PATH, "a") as f:
        f.write(entry)
    print("🔱 ÉVÉNEMENT GRAVÉ : " + message_clean)
    return True


if __name__ == "__main__":
    enregistrer_evenement("Éveil de l'Alliée réussi sur MacBook 2010")
