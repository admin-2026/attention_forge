import sys
import os
from api_key_loader import load_api_key
from config_loader import load_project_config, load_role_config
from context_loader import load_context
from openai_client import generate_response
from chat_logger import log_chat
from response_parser import process_openai_response

def main():
    # Determine the project configuration file path
    project_config_path = sys.argv[1] if len(sys.argv) > 1 else "project_config.yaml"

    # Determine the role name (default if not specified)
    role_name = sys.argv[2] if len(sys.argv) > 2 else "default"

    # Verify the project config file exists
    if not os.path.isfile(project_config_path):
        print(f"Error: Project config file '{project_config_path}' not found.")
        sys.exit(1)

    # Load configurations and API key
    try:
        project_config = load_project_config(project_config_path)
        role_config = load_role_config(role_name)
        api_key = load_api_key()
    except Exception as e:
        print(e)
        sys.exit(1)

    # Get user input
    user_message = input("Enter your message (or type 'exit' to quit): ").strip().lower()

    # Check if user wants to exit
    if user_message == "exit":
        print("Exiting the program. No request sent to OpenAI.")
        sys.exit(0)

    # Load context files (optional)
    context_files = load_context()
    context_text = "\n".join(content for content in context_files.values()) if context_files else ""

    # Modify developer message to include code context
    if context_text:
        role_config["developer_message"] += f"\n\nHere are some relevant code files:\n\n{context_text}"

    # Generate response using OpenAI API
    try:
        request_data, response_data, assistant_reply = generate_response(
            api_key, project_config, role_config, user_message
        )
        print("OpenAI Assistant:", assistant_reply)

        # Log the full chat
        log_chat(project_config["log_file"], request_data, response_data)

        # Process response for file updates
        process_openai_response(assistant_reply)

    except Exception as e:
        print("An error occurred while communicating with OpenAI:", e)

if __name__ == "__main__":
    main()
