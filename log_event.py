import datetime
import os

LOG_PATH = "DATA/LOGS_SOUVERAINS/session_log.txt"

def enregistrer_evenement(message):
    if not isinstance(message, str):
        message = str(message)

    # Sanitize message to prevent Log Injection (CWE-117)
    clean_message = message.replace("\r", " ").replace("\n", " ")

    log_path = LOG_PATH
    parent_dir = os.path.dirname(log_path)
    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {clean_message}\n"
    
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(entry)
    print("🔱 ÉVÉNEMENT GRAVÉ : " + clean_message)

if __name__ == "__main__":
    enregistrer_evenement("Éveil de l'Alliée réussi sur MacBook 2010")
