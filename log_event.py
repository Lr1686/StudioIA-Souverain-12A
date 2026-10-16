import datetime
import os

def enregistrer_evenement(message):
    if not isinstance(message, str):
        print("⚠️ ERREUR : Le message doit être une chaîne de caractères.")
        return False

    # Security: Sanitize newlines and control characters to prevent log injection (CWE-117)
    message_clean = message.replace('\r', ' ').replace('\n', ' ').strip()

    log_path = "DATA/LOGS_SOUVERAINS/session_log.txt"
    log_dir = os.path.dirname(log_path)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = "[" + timestamp + "] " + message_clean + "\n"
    
    with open(log_path, "a") as f:
        f.write(entry)
    print("🔱 ÉVÉNEMENT GRAVÉ : " + message_clean)
    return True

if __name__ == "__main__":
    enregistrer_evenement("Éveil de l'Alliée réussi sur MacBook 2010")
