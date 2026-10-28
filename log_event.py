import datetime
import os

LOG_PATH = "DATA/LOGS_SOUVERAINS/session_log.txt"

def enregistrer_evenement(message):
    """
    Enregistre un événement dans les logs de session.
    Valide et assainit le message pour éviter les injections de logs (CRLF injection).
    """
    if not isinstance(message, str):
        print("⚠️ ERREUR : Le message de log doit être une chaîne de caractères.")
        return False

    message_clean = message.strip()
    if not message_clean:
        print("⚠️ ERREUR : Le message de log ne peut pas être vide.")
        return False

    # Sanitization: Neutralize line breaks and non-printable control characters
    sanitized_chars = []
    for char in message_clean:
        code = ord(char)
        if char in ("\n", "\r"):
            sanitized_chars.append(" ")
        elif code < 32 or code == 127:
            sanitized_chars.append("?")
        else:
            sanitized_chars.append(char)

    sanitized_message = "".join(sanitized_chars)

    log_dir = os.path.dirname(LOG_PATH)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {sanitized_message}\n"

    with open(LOG_PATH, "a") as f:
        f.write(entry)

    print("🔱 ÉVÉNEMENT GRAVÉ : " + sanitized_message)
    return True

if __name__ == "__main__":
    enregistrer_evenement("Éveil de l'Alliée réussi sur MacBook 2010")
