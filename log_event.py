import datetime
import os

def enregistrer_evenement(message):
    log_path = "DATA/LOGS_SOUVERAINS/session_log.txt"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = "[" + timestamp + "] " + message + "\n"
    
    # Performance Optimization: Guard directory creation with os.path.exists check.
    # Avoids syscall overhead on every log write when the log directory already exists.
    log_dir = os.path.dirname(log_path)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    with open(log_path, "a") as f:
        f.write(entry)
    print("🔱 ÉVÉNEMENT GRAVÉ : " + message)

if __name__ == "__main__":
    enregistrer_evenement("Éveil de l'Alliée réussi sur MacBook 2010")
