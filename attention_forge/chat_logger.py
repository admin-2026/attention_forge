import os
import json
import logging
from attention_forge.config_loader import load_project_config

# Ensure build directory exists
BUILD_DIR = "attention_forge_build/"
if not os.path.exists(BUILD_DIR):
    os.makedirs(BUILD_DIR)

def log_chat(log_file, request_data, response_data):
    """Logs the full request and response to a file inside attention_forge_build."""
    log_path = os.path.join(BUILD_DIR, os.path.basename(log_file))

    logging.basicConfig(filename=log_path, level=logging.INFO, format="%(asctime)s - %(message)s")

    log_entry = {
        "timestamp": logging.Formatter().formatTime(logging.makeLogRecord({})),
        "request": request_data,
        "response": response_data
    }

    with open(log_path, "a", encoding="utf-8") as log:
        log.write(json.dumps(log_entry, indent=4) + "\n" + "=" * 80 + "\n")

    print(f"📜 Chat log saved to {log_path}")
