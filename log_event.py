import datetime
import os

LOG_PATH = "DATA/LOGS_SOUVERAINS/session_log.txt"
MAX_LOG_LENGTH = 1000

def enregistrer_evenement(message):
    if not isinstance(message, str):
        message = str(message)

    # Security input validation & sanitization (CWE-117: Log Injection)
    # Strip unprintable control characters and replace newlines to prevent log forging
    clean_chars = []
    for char in message:
        if char in ('\r', '\n'):
            clean_chars.append(' ')
        elif ord(char) < 32 or ord(char) == 127:
            continue
        else:
            clean_chars.append(char)

    # Collapse multiple consecutive spaces resulting from newline replacement
    clean_message = " ".join("".join(clean_chars).split()).strip()
    if len(clean_message) > MAX_LOG_LENGTH:
        clean_message = clean_message[:MAX_LOG_LENGTH] + "... [TRUNCATED]"

    dir_path = os.path.dirname(LOG_PATH)
    if dir_path and not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {clean_message}\n"
    
    with open(LOG_PATH, "a") as f:
        f.write(entry)
    print("🔱 ÉVÉNEMENT GRAVÉ : " + clean_message)

if __name__ == "__main__":
    enregistrer_evenement("Éveil de l'Alliée réussi sur MacBook 2010")
