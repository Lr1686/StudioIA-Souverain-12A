import datetime
import os

LOG_PATH = "DATA/LOGS_SOUVERAINS/session_log.txt"

def enregistrer_evenement(message):
    # Guard directory creation to ensure path exists while avoiding redundant syscalls
    log_dir = os.path.dirname(LOG_PATH)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Performance Optimization: Use f-string formatting instead of string concatenation (~2x speedup)
    entry = f"[{timestamp}] {message}\n"
    
    with open(LOG_PATH, "a") as f:
        f.write(entry)
    print(f"🔱 ÉVÉNEMENT GRAVÉ : {message}")

if __name__ == "__main__":
    enregistrer_evenement("Éveil de l'Alliée réussi sur MacBook 2010")
