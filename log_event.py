import datetime
import json
import os

def enregistrer_evenement(message, log_path="DATA/LOGS_SOUVERAINS/session_log.txt"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Sanitize message to prevent log injection (CWE-117)
    sanitized_message = str(message).replace("\r", " ").replace("\n", " ")
    entry = "[" + timestamp + "] " + sanitized_message + "\n"
    
    dirname = os.path.dirname(log_path)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    with open(log_path, "a") as f:
        f.write(entry)
    print("🔱 ÉVÉNEMENT GRAVÉ : " + sanitized_message)

if __name__ == "__main__":
    enregistrer_evenement("Éveil de l'Alliée réussi sur MacBook 2010")
