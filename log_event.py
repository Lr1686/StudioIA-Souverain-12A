import datetime
import os

LOG_PATH = "DATA/LOGS_SOUVERAINS/session_log.txt"

def enregistrer_evenement(message):
    # Sanitize message to prevent log injection via unescaped newlines
    sanitized_message = str(message).replace("\r", "\\r").replace("\n", "\\n")

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {sanitized_message}\n"

    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    
    with open(LOG_PATH, "a") as f:
        f.write(entry)
    print("🔱 ÉVÉNEMENT GRAVÉ : " + sanitized_message)

if __name__ == "__main__":
    enregistrer_evenement("Éveil de l'Alliée réussi sur MacBook 2010")
