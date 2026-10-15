import datetime
import os

LOG_PATH = "DATA/LOGS_SOUVERAINS/session_log.txt"

def enregistrer_evenement(message):
    parent_dir = os.path.dirname(LOG_PATH)
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = "[" + timestamp + "] " + message + "\n"
    
    with open(LOG_PATH, "a") as f:
        f.write(entry)
    print("🔱 ÉVÉNEMENT GRAVÉ : " + message)

if __name__ == "__main__":
    enregistrer_evenement("Éveil de l'Alliée réussi sur MacBook 2010")
