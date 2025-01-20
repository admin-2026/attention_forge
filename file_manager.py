import os
import shutil
import datetime

BUILD_DIR = "attention_forge_build/"
BACKUP_DIR = os.path.join(BUILD_DIR, "backup/")

def ensure_backup_directory():
    """Ensure the attention_forge_build/backup directory exists."""
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

def backup_file(file_path):
    """Back up the original file before modifying it."""
    ensure_backup_directory()
    if os.path.exists(file_path):
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        backup_path = os.path.join(BACKUP_DIR, f"{os.path.basename(file_path)}_{timestamp}.bak")
        shutil.copy(file_path, backup_path)
        print(f"🔄 Backup created: {backup_path}")
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
