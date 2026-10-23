import datetime
import os

def enregistrer_evenement(message):
    if not isinstance(message, str):
        message = str(message)

    # Sanitize message to prevent log injection (CWE-117)
    clean_message = message.replace('\r', '\\r').replace('\n', '\\n')

    log_path = "DATA/LOGS_SOUVERAINS/session_log.txt"
    parent_dir = os.path.dirname(log_path)
    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {clean_message}\n"
    
    with open(log_path, "a") as f:
        f.write(entry)
    print("🔱 ÉVÉNEMENT GRAVÉ : " + clean_message)

if __name__ == "__main__":
    enregistrer_evenement("Éveil de l'Alliée réussi sur MacBook 2010")
