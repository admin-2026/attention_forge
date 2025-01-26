from attention_forge.chain_steps.step import Step
import shutil
from attention_forge.file_manager import load_backup_log, get_latest_run_id

class FileReverter(Step):
    def run(self, input_data=None):
        backup_log = load_backup_log()
        latest_run_id = get_latest_run_id()

        if not latest_run_id:
            print("⚠️ No backups found.")
            return

        # Get all backups from the latest run_id
        latest_backups = [entry for entry in backup_log if entry["run_id"] == latest_run_id]

        if not latest_backups:
            print("⚠️ No backups available for the latest run.")
            return

        # Display options
        print("\n🔄 Files available for reversion:")
        for i, entry in enumerate(latest_backups):
            print(f"{i + 1}. {entry['original_file']} (Backup: {entry['backup_file']})")

        # Ask user to select files
        choice = input("\nEnter the numbers of the files to revert (comma-separated, or 'cancel' to abort): ").strip()

        if choice.lower() == "cancel":
            print("❌ Reversion cancelled.")
            return

        try:
            # Split by comma and convert to integers
            indexes = [int(idx.strip()) - 1 for idx in choice.split(',')]
            invalid_indexes = [idx for idx in indexes if idx < 0 or idx >= len(latest_backups)]

            if invalid_indexes:
                print("⚠️ Invalid choice(s). Please enter valid numbers.")
                return

            # Restore each selected file
            for index in indexes:
                selected_entry = latest_backups[index]
                backup_path = selected_entry["backup_file"]
                original_path = selected_entry["original_file"]

                # Restore file
                shutil.copy(backup_path, original_path)
                print(f"♻️ Reverted '{original_path}' to backup: {backup_path}")

        except ValueError:
            print("⚠️ Invalid input. Please enter numbers separated by commas.")