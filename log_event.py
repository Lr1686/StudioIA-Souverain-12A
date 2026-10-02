import datetime
import os

def enregistrer_evenement(message):
    log_path = "DATA/LOGS_SOUVERAINS/session_log.txt"
    # Sanitize message to prevent log injection (CWE-117) by replacing newline characters
    sanitized_message = str(message).replace("\r", " ").replace("\n", " ")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = "[" + timestamp + "] " + sanitized_message + "\n"
    
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, "a") as f:
        f.write(entry)
    print("🔱 ÉVÉNEMENT GRAVÉ : " + message)

if __name__ == "__main__":
    enregistrer_evenement("Éveil de l'Alliée réussi sur MacBook 2010")
