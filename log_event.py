import datetime
import os

LOG_PATH = "DATA/LOGS_SOUVERAINS/session_log.txt"

def enregistrer_evenement(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Performance optimization: Use fast f-string formatting instead of string concatenation,
    # and conditionally create log directory only if missing to prevent unnecessary syscall overhead.
    entry = f"[{timestamp}] {message}\n"
    
    log_dir = os.path.dirname(LOG_PATH)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    with open(LOG_PATH, "a") as f:
        f.write(entry)
    print("🔱 ÉVÉNEMENT GRAVÉ : " + message)

if __name__ == "__main__":
    enregistrer_evenement("Éveil de l'Alliée réussi sur MacBook 2010")
