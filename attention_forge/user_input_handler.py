from attention_forge.file_manager import revert_file

def get_user_message():
    """
    Handles user input and checks for exit or revert commands.
    Returns the user message if valid, otherwise executes the respective action.
    """
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
