import datetime
import os

LOG_PATH = "DATA/LOGS_SOUVERAINS/session_log.txt"

def enregistrer_evenement(message, log_path=None):
    if log_path is None:
        log_path = LOG_PATH

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {message}\n"
    
    # EAFP pattern for log file writing:
    # Attempt to write to log file directly and catch FileNotFoundError to lazily create parent directories on demand.
    # This ensures robust logging while optimizing string construction with f-strings.
    try:
        with open(log_path, "a") as f:
            f.write(entry)
    except FileNotFoundError:
        parent_dir = os.path.dirname(log_path)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)
        with open(log_path, "a") as f:
            f.write(entry)

    print("🔱 ÉVÉNEMENT GRAVÉ : " + message)

if __name__ == "__main__":
    enregistrer_evenement("Éveil de l'Alliée réussi sur MacBook 2010")
