import os


def load_config():
    log_path = os.getenv("LOG_FILE_PATH", "").strip()
    threshold_raw = os.getenv("THRESHOLD", "5").strip()

    telegram_token = os.getenv("TELEGRAM_TOKEN", "").strip()
    chat_id = os.getenv("CHAT_ID", "").strip()

    if not log_path:
        raise ValueError(
            "LOG_FILE_PATH is missing. Set it in your .env file."
        )

    try:
        threshold = int(threshold_raw)
    except ValueError:
        raise ValueError(
            "THRESHOLD must be a valid integer."
        )

    if threshold < 1:
        raise ValueError(
            "THRESHOLD must be greater than zero."
        )

    if bool(telegram_token) != bool(chat_id):
        raise ValueError(
            "Set both TELEGRAM_TOKEN and CHAT_ID, "
            "or leave both empty."
        )

    return {
        "log_path": log_path,
        "threshold": threshold,
    }
