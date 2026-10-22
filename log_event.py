import datetime
import os

LOG_PATH = "DATA/LOGS_SOUVERAINS/session_log.txt"
MAX_LOG_LENGTH = 500

def enregistrer_evenement(message):
    # Validation de sécurité du type
    if not isinstance(message, str):
        print("⚠️ ERREUR : Le message doit être une chaîne de caractères.")
        return False

    message_clean = message.strip()
    if not message_clean:
        print("⚠️ ERREUR : Le message ne peut pas être vide.")
        return False

    if len(message_clean) > MAX_LOG_LENGTH:
        print(f"⚠️ ERREUR : Le message dépasse la longueur maximale autorisée ({MAX_LOG_LENGTH} caractères).")
        return False

    # Prévention contre l'injection de log (Log Injection / CRLF Injection)
    # Remplacement des caractères de contrôle et sauts de ligne par des espaces
    sanitized_message = "".join(c if ord(c) >= 32 and ord(c) != 127 else " " for c in message_clean)

    # Assurer l'existence du dossier de logs
    parent_dir = os.path.dirname(LOG_PATH)
    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {sanitized_message}\n"
    
    with open(LOG_PATH, "a") as f:
        f.write(entry)
    print("🔱 ÉVÉNEMENT GRAVÉ : " + sanitized_message)
    return True

if __name__ == "__main__":
    enregistrer_evenement("Éveil de l'Alliée réussi sur MacBook 2010")
