import json
import logging

def log_chat(log_file, request_data, response_data):
    """Logs the full request and response to a file."""
    logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s - %(message)s")

    log_entry = {
        "timestamp": logging.Formatter().formatTime(logging.makeLogRecord({})),
        "request": request_data,
        "response": response_data
    }

    with open(log_file, "a") as log:
        log.write(json.dumps(log_entry, indent=4) + "\n" + "=" * 80 + "\n")