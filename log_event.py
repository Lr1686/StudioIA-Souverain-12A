import datetime
import os

LOG_PATH = "DATA/LOGS_SOUVERAINS/session_log.txt"
MAX_LOG_LENGTH = 500

def enregistrer_evenement(message):
    log_file_path = LOG_PATH

    if not isinstance(message, str):
        message = str(message)

    # Sanitize newline and carriage return characters to prevent log forging
    message_clean = message.replace('\r', ' ').replace('\n', ' ')

    # Filter out control characters (ASCII < 32 except space, ASCII 127)
    message_clean = "".join(
        c for c in message_clean if ord(c) >= 32 and ord(c) != 127
    ).strip()

    # Truncate message to MAX_LOG_LENGTH to prevent log bloat / DoS
    if len(message_clean) > MAX_LOG_LENGTH:
        message_clean = message_clean[:MAX_LOG_LENGTH]

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = "[" + timestamp + "] " + message_clean + "\n"

    parent_dir = os.path.dirname(log_file_path)
    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)

    with open(log_file_path, "a") as f:
        f.write(entry)
    print("🔱 ÉVÉNEMENT GRAVÉ : " + message_clean)

if __name__ == "__main__":
    enregistrer_evenement("Éveil de l'Alliée réussi sur MacBook 2010")
