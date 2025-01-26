import os
import shutil
import datetime
import json

BUILD_DIR = ".attention_forge/"
BACKUP_DIR = os.path.join(BUILD_DIR, "backup/")
BACKUP_LOG = os.path.join(BUILD_DIR, "backup_log.json")

# Global variable for Run ID
run_id = None

def set_run_id(new_run_id):
    """Set the run ID for the current execution."""
    global run_id
    run_id = new_run_id

def ensure_directories():
    """Ensure required directories and backup log file exist."""
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    if not os.path.exists(BACKUP_LOG):
        with open(BACKUP_LOG, "w", encoding="utf-8") as log_file:
            json.dump([], log_file)  # Initialize as empty list

def load_backup_log():
    """Load the backup log from JSON."""
    if not os.path.exists(BACKUP_LOG):
        return []
    try:
        with open(BACKUP_LOG, "r", encoding="utf-8") as log_file:
            return json.load(log_file)
    except json.JSONDecodeError:
        return []  # Return empty list if JSON is malformed

def save_backup_log(log_entries):
    """Save the backup log to JSON."""
    with open(BACKUP_LOG, "w", encoding="utf-8") as log_file:
        json.dump(log_entries, log_file, indent=4)

def get_latest_run_id():
    """Retrieve the latest run_id from the backup log."""
    backup_log = load_backup_log()
    if not backup_log:
        return None
    return backup_log[-1]["run_id"]  # The latest entry's run_id

def backup_file(file_path):
    """Back up the original file before modifying it and log the operation."""
    ensure_directories()
    backup_log = load_backup_log()

    if os.path.exists(file_path):
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        backup_filename = f"{os.path.basename(file_path)}_{timestamp}.bak"
        backup_path = os.path.join(BACKUP_DIR, backup_filename)
        shutil.copy(file_path, backup_path)

        # Log the backup operation with run ID
        log_entry = {
            "run_id": run_id,  # Attach Run ID
            "original_file": file_path,
            "backup_file": backup_path,
            "timestamp": timestamp
        }
        backup_log.append(log_entry)
        save_backup_log(backup_log)

        print(f"🔄 Backup created: {backup_path} (Run ID: {run_id})")
    else:
        print(f"⚠️ Warning: File '{file_path}' does not exist, so no backup was created.")

def update_file(file_path, new_content):
    """Update a file with new content after backing it up."""
    backup_file(file_path)
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(new_content)
        print(f"✅ Updated file: {file_path}")
    except Exception as e:
        print(f"🚨 Error updating file '{file_path}': {e}")

