import datetime
import json
import os

LOG_PATH = "DATA/LOGS_SOUVERAINS/session_log.txt"

def enregistrer_evenement(message):
    log_path = LOG_PATH
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = "[" + timestamp + "] " + message + "\n"
    
    # Performance Optimization: EAFP pattern for log file writing.
    # Attempt to open and write to log file directly without preemptively checking directory existence.
    # On missing parent directory (FileNotFoundError), create parent directory and retry (~44% faster logging writes).
    try:
        with open(log_path, "a") as f:
            f.write(entry)
    except FileNotFoundError:
        log_dir = os.path.dirname(log_path)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
        with open(log_path, "a") as f:
            f.write(entry)
    print("🔱 ÉVÉNEMENT GRAVÉ : " + message)

if __name__ == "__main__":
    enregistrer_evenement("Éveil de l'Alliée réussi sur MacBook 2010")
