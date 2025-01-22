from attention_forge.file_manager import revert_file
import os

def get_user_message(user_message_file_path):
    """
    Handles user input, and checks for exit or revert commands.
    Tries to load user message from a given file path if it exists and is not empty.
    If a message is found, prompts for confirmation before proceeding.
    """

    # Try to read from user message file if defined and not empty
    if user_message_file_path and os.path.isfile(user_message_file_path):
        with open(user_message_file_path, "r", encoding="utf-8") as file:
            user_message = file.read().strip()
            if user_message:
                print(f"📄 Loaded user message from file: {user_message_file_path}")
                confirmation = input("Do you want to use this message? (yes/no): ").strip().lower()

                if confirmation == "yes":
                    return user_message
                else:
                    print("Please enter your message:")

    # If file reading fails, file is empty, or user opts not to use file message, prompt for input
    user_message = input("Enter your message (or type 'exit' to quit, 'revert' to restore a file): ").strip()

    # Handle exit command
    if user_message.lower() == "exit":
        print("Exiting the program. No request sent to OpenAI.")
        exit(0)

    # Handle revert command
    if user_message.lower() == "revert":
        revert_file()
        exit(0)

    return user_message