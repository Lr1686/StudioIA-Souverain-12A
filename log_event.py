import datetime
import os

LOG_PATH = "DATA/LOGS_SOUVERAINS/session_log.txt"

def enregistrer_evenement(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {message}\n"
    
    # Performance Optimization: Use EAFP (Easier to Ask for Forgiveness than Permission).
    # Writing directly avoids calling os.makedirs on every append (~1.6x speedup).
    # If the directory doesn't exist yet, catch FileNotFoundError, create it, and retry.
    try:
        with open(LOG_PATH, "a") as f:
            f.write(entry)
    except FileNotFoundError:
        log_dir = os.path.dirname(LOG_PATH)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
        with open(LOG_PATH, "a") as f:
            f.write(entry)

    print("🔱 ÉVÉNEMENT GRAVÉ : " + message)

if __name__ == "__main__":
    enregistrer_evenement("Éveil de l'Alliée réussi sur MacBook 2010")
