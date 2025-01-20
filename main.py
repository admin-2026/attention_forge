import sys
import os
import uuid  # Import for generating unique Run IDs
from api_key_loader import load_api_key
from config_loader import load_project_config, load_role_config
from context_loader import load_context
from openai_client import generate_response
from chat_logger import log_chat
from response_parser import process_openai_response
from user_input_handler import get_user_message
from file_manager import set_run_id

def main():
    # Generate a unique run ID for this execution
    run_id = str(uuid.uuid4())  # Generate a UUID for the run
    set_run_id(run_id)  # Pass Run ID to file manager for logging

    # Determine the project configuration file path
    project_config_path = sys.argv[1] if len(sys.argv) > 1 else "attention_forge_project.yaml"

    # Determine the role name (default if not specified)
    role_name = sys.argv[2] if len(sys.argv) > 2 else "default"

    # Verify the project config file exists
    if not os.path.isfile(project_config_path):
        print(f"Error: Project config file '{project_config_path}' not found.")
        sys.exit(1)

    # Load configurations
    try:
        project_config = load_project_config(project_config_path)
        role_config = load_role_config(role_name)
        api_key_path = project_config.get("api_key_file", "api-key")  # Get API key location
        api_key = load_api_key(api_key_path)  # Pass API key location directly
    except Exception as e:
        print(e)
        sys.exit(1)

    print(f"🆔 Run ID: {run_id}")

    # Get user input using the new handler
    user_message = get_user_message()

    # Load context files, passing the API key path to ensure it's ignored
    context_files = load_context(api_key_path)
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

        # Extract token usage safely
        token_usage = response_data["usage"]
        print(f"📊 Token Usage - Prompt: {token_usage['prompt_tokens']}, "
              f"Completion: {token_usage['completion_tokens']}, "
              f"Total: {token_usage['total_tokens']}")

        # Log the full chat
        log_chat(project_config["log_file"], request_data, response_data)

        # Process response for file updates
        process_openai_response(assistant_reply)

    except Exception as e:
        print("An error occurred while communicating with OpenAI:", e)

if __name__ == "__main__":
    main()
