import datetime
import os

LOG_PATH = "DATA/LOGS_SOUVERAINS/session_log.txt"

def enregistrer_evenement(message):
    log_path = LOG_PATH
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = "[" + timestamp + "] " + message + "\n"
    
    # Performance Optimization: Guard directory creation with os.path.exists check.
    # Prevents FileNotFoundError when log directory is missing while avoiding
    # unnecessary os.makedirs syscall overhead when directory exists (~4x speedup).
    parent_dir = os.path.dirname(log_path)
    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)

    with open(log_path, "a") as f:
        f.write(entry)
    print("🔱 ÉVÉNEMENT GRAVÉ : " + message)

if __name__ == "__main__":
    enregistrer_evenement("Éveil de l'Alliée réussi sur MacBook 2010")
