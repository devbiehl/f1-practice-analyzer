# logging_config.py
import logging
import os
from datetime import datetime
import re

def clean_filename(name):
    return re.sub(r'[^\w\w-]', '_', name.strip().lower())

def setup_logger(track_name="unknowntrack", session_name="unknownsession", log_level=logging.INFO):
    os.makedirs("logs", exist_ok=True)

    clean_track = clean_filename(track_name)
    clean_session = clean_filename(session_name)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    log_filename = f"logs/f1_{timestamp}.log"

    logger = logging.getLogger("f1_logger")
    logger.setLevel(log_level)

    if not logger.handlers:
        file_handler = logging.FileHandler(log_filename)
        file_handler.setLevel(log_level)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)

        formatter = logging.Formatter('%(asctime)s — %(levelname)s — %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
