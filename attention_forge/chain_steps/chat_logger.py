import os
import json
import logging
from datetime import datetime

# Ensure build directory exists
BUILD_DIR = ".attention_forge/"
LOG_DIR = os.path.join(BUILD_DIR, "logs")

# Ensure logs directory exists
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

class ChatLogger:
    def __init__(self, log_file):
        # Determine the base name of the log file
        base_log_name = os.path.basename(log_file)
        self.base_log_name = os.path.splitext(base_log_name)[0]

    def _get_daily_log_path(self):
        # Generate today's date string
        today_str = datetime.now().strftime('%Y-%m-%d')
        # Construct the daily log file path
        daily_log_file = f"{self.base_log_name}_{today_str}.log"
        return os.path.join(LOG_DIR, daily_log_file)

    def log_chat(self, request_data, response_data, client_name, model_name):
        """Logs the full request and response along with client and model info."""
        log_path = self._get_daily_log_path()
        
        # Ensure the logger is configured for the specific file
        logging.basicConfig(filename=log_path, level=logging.INFO,
                            format="%(asctime)s - %(message)s")

        log_entry = {
            "timestamp": logging.Formatter().formatTime(logging.makeLogRecord({})),
            "client_name": client_name,
            "model_name": model_name,
            "request": request_data,
            "response": response_data
        }

        with open(log_path, "a", encoding="utf-8") as log:
            log.write(json.dumps(log_entry, indent=4) + "\n" + "=" * 80 + "\n")

        print(f"📜 Chat log saved to {log_path}")