import os

def enregistrer_evenement(message, log_path="DATA/LOGS_SOUVERAINS/session_log.txt"):
    if not isinstance(message, str):
        message = str(message)

    # Sanitize message to prevent log injection (replace control characters and newlines)
    clean_message = "".join(c if (ord(c) >= 32 and ord(c) != 127) else " " for c in message).strip()

    parent_dir = os.path.dirname(log_path)
    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)

    import datetime
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = "[" + timestamp + "] " + clean_message + "\n"
    
    with open(log_path, "a") as f:
        f.write(entry)
    print("🔱 ÉVÉNEMENT GRAVÉ : " + clean_message)

if __name__ == "__main__":
    enregistrer_evenement("Éveil de l'Alliée réussi sur MacBook 2010")
