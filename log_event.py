import datetime
import os

LOG_PATH = "DATA/LOGS_SOUVERAINS/session_log.txt"

def enregistrer_evenement(message):
    # Security: Input validation
    if not isinstance(message, str):
        print("⚠️ ERREUR : Le message de log doit être une chaîne de caractères.")
        return False

    message_clean = message.strip()
    if not message_clean:
        print("⚠️ ERREUR : Le message de log ne peut pas être vide.")
        return False

    # Security: Prevent Log Injection (CWE-117) by sanitizing newlines and control chars
    clean_msg = "".join(c if ord(c) >= 32 and ord(c) != 127 else " " for c in message_clean)

    log_path = LOG_PATH
    log_dir = os.path.dirname(log_path)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {clean_msg}\n"
    
    with open(log_path, "a") as f:
        f.write(entry)
    print("🔱 ÉVÉNEMENT GRAVÉ : " + clean_msg)
    return True

if __name__ == "__main__":
    enregistrer_evenement("Éveil de l'Alliée réussi sur MacBook 2010")
