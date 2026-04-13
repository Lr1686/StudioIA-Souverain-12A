import datetime
import json
import os

def enregistrer_evenement(message):
    log_path = "DATA/LOGS_SOUVERAINS/session_log.txt"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = "[" + timestamp + "] " + message + "\n"
    
    with open(log_path, "a") as f:
        f.write(entry)
    print("🔱 ÉVÉNEMENT GRAVÉ : " + message)

if __name__ == "__main__":
    enregistrer_evenement("Éveil de l'Alliée réussi sur MacBook 2010")
