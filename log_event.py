import datetime
import os

LOG_PATH = "DATA/LOGS_SOUVERAINS/session_log.txt"

def enregistrer_evenement(message, log_path=None):
    if log_path is None:
        log_path = LOG_PATH

    # Performance & Reliability Optimization: Ensure parent log directory exists before writing.
    # Checking directory existence avoids unnecessary mkdir syscalls on existing paths while preventing
    # FileNotFoundError crashes when logging to an uninitialized path.
    parent_dir = os.path.dirname(log_path)
    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {message}\n"
    
    with open(log_path, "a") as f:
        f.write(entry)
    print(f"🔱 ÉVÉNEMENT GRAVÉ : {message}")

if __name__ == "__main__":
    enregistrer_evenement("Éveil de l'Alliée réussi sur MacBook 2010")
