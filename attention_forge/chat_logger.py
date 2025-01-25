import os
import json
import logging

# Ensure build directory exists
BUILD_DIR = "attention_forge_build/"
if not os.path.exists(BUILD_DIR):
    os.makedirs(BUILD_DIR)

class ChatLogger:
    def __init__(self, log_file):
        self.log_path = os.path.join(BUILD_DIR, os.path.basename(log_file))
        logging.basicConfig(filename=self.log_path, level=logging.INFO, format="%(asctime)s - %(message)s")

    def log_chat(self, request_data, response_data, client_name, model_name):
        """Logs the full request and response along with client and model info."""
        log_entry = {
            "timestamp": logging.Formatter().formatTime(logging.makeLogRecord({})),
            "client_name": client_name,
            "model_name": model_name,
            "request": request_data,
            "response": response_data
        }

        with open(self.log_path, "a", encoding="utf-8") as log:
            log.write(json.dumps(log_entry, indent=4) + "\n" + "=" * 80 + "\n")

        print(f"📜 Chat log saved to {self.log_path}")