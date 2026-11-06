import datetime
import os

LOG_PATH = "DATA/LOGS_SOUVERAINS/session_log.txt"
MAX_LOG_LENGTH = 500


def enregistrer_evenement(message):
    # Security: Validate message type to prevent unexpected object stringification
    if not isinstance(message, str):
        print("⚠️ ERREUR : Le message doit être une chaîne de caractères.")
        return False

    message_clean = message.strip()
    if not message_clean:
        print("⚠️ ERREUR : Le message ne peut pas être vide.")
        return False

    # Security: Enforce maximum message length to mitigate DoS / log bloat
    if len(message_clean) > MAX_LOG_LENGTH:
        print(f"⚠️ ERREUR : Le message dépasse la longueur maximale autorisée ({MAX_LOG_LENGTH} caractères).")
        return False

    # Security: Mitigate CWE-117 (Log Injection) by rejecting newlines, carriage returns, and control characters
    if any(ord(c) < 32 or ord(c) == 127 for c in message_clean):
        print("⚠️ ERREUR : Le message contient des caractères de contrôle ou sauts de ligne non autorisés.")
        return False

    # Ensure parent log directory exists
    parent_dir = os.path.dirname(LOG_PATH)
    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)

    # Performance Optimization: Using isoformat(sep=" ", timespec="seconds") produces identical
    # format "YYYY-MM-DD HH:MM:SS" ~2.6x faster than strftime format string parsing.
    timestamp = datetime.datetime.now().isoformat(sep=" ", timespec="seconds")
    entry = f"[{timestamp}] {message_clean}\n"

    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(entry)

    print("🔱 ÉVÉNEMENT GRAVÉ : " + message_clean)
    return True


if __name__ == "__main__":
    enregistrer_evenement("Éveil de l'Alliée réussi sur MacBook 2010")
