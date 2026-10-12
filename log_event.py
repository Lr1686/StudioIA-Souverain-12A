import datetime
import os

def enregistrer_evenement(message, log_path="DATA/LOGS_SOUVERAINS/session_log.txt"):

    # Performance Optimization: Guard directory creation with os.path.exists.
    # Bypasses unnecessary os.makedirs overhead when the target directory already exists.
    parent_dir = os.path.dirname(log_path)
    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Performance Optimization: F-strings build string representations via BUILD_STRING instruction
    # avoiding multiple BINARY_OP (+) allocations (~1.6x faster string formatting).
    entry = f"[{timestamp}] {message}\n"
    
    with open(log_path, "a") as f:
        f.write(entry)
    print(f"🔱 ÉVÉNEMENT GRAVÉ : {message}")

if __name__ == "__main__":
    enregistrer_evenement("Éveil de l'Alliée réussi sur MacBook 2010")
