import datetime
import os

LOG_PATH = "DATA/LOGS_SOUVERAINS/session_log.txt"

def enregistrer_evenement(message):
    # Security: Sanitize input to prevent Log Injection / Log Forgery (CWE-117)
    if not isinstance(message, str):
        message = str(message)

    # Sanitize newlines and carriage returns to prevent fake log entry insertion
    clean_message = message.replace("\r", " ").replace("\n", " ").strip()

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = "[" + timestamp + "] " + clean_message + "\n"

    parent_dir = os.path.dirname(LOG_PATH)
    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)

    with open(LOG_PATH, "a") as f:
        f.write(entry)
    print("🔱 ÉVÉNEMENT GRAVÉ : " + clean_message)

if __name__ == "__main__":
    enregistrer_evenement("Éveil de l'Alliée réussi sur MacBook 2010")
