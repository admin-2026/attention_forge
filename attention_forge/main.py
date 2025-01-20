import sys
import os
import uuid  # Generate Run IDs

# Import required modules from the attention_forge package
from attention_forge.api_key_loader import load_api_key
from attention_forge.config_loader import load_project_config, load_role_config
from attention_forge.context_loader import load_context
from attention_forge.openai_client import generate_response
from attention_forge.chat_logger import log_chat
from attention_forge.response_parser import process_openai_response
from attention_forge.user_input_handler import get_user_message
from attention_forge.file_manager import set_run_id

def main():
    """
    Main function for running the Attention Forge assistant.

    - Loads configurations from YAML files.
    - Handles user input and retrieves relevant code context.
    - Sends a request to OpenAI with developer/assistant messages.
    - Logs chat history and processes file updates.
    - Displays token usage for tracking API costs.
    """

    # Generate a unique run ID for logging and backups
    run_id = str(uuid.uuid4())
    set_run_id(run_id)  # Store Run ID for tracking operations

    # Determine the project configuration file path
    project_config_path = sys.argv[1] if len(sys.argv) > 1 else "attention_forge_project.yaml"

    # Determine the role configuration name (default role if not specified)
    role_name = sys.argv[2] if len(sys.argv) > 2 else "default"

    # Ensure the project configuration file exists
    if not os.path.isfile(project_config_path):
        print(f"Error: Project config file '{project_config_path}' not found.")
        sys.exit(1)

    # Load configurations (handling potential errors)
    try:
        project_config = load_project_config(project_config_path)
        role_config = load_role_config(role_name)
        api_key_path = project_config.get("api_key_file", "api-key")  # Retrieve API key file path
        api_key = load_api_key(api_key_path)  # Load API key
    except Exception as e:
        print(f"Configuration error: {e}")
        sys.exit(1)

    print(f"🆔 Run ID: {run_id}")  # Display Run ID for tracking

    # Get user message through input handler
    user_message = get_user_message()

    # Load relevant context files while ensuring API key is excluded
    context_files = load_context(api_key_path)
    context_text = "\n".join(content for content in context_files.values()) if context_files else ""

    # Append context information to the developer message
    if context_text:
        role_config["developer_message"] += f"\n\nHere are some relevant code files:\n\n{context_text}"

    # Communicate with OpenAI to generate a response
    try:
        request_data, response_data, assistant_reply = generate_response(
            api_key, project_config, role_config, user_message
        )
        print("OpenAI Assistant:", assistant_reply)  # Display assistant's response

        # Extract token usage and print it
        token_usage = response_data["usage"]
        print(f"📊 Token Usage - Prompt: {token_usage['prompt_tokens']}, "
              f"Completion: {token_usage['completion_tokens']}, "
              f"Total: {token_usage['total_tokens']}")

        # Log chat history to file
        log_chat(project_config["log_file"], request_data, response_data)

        # Process OpenAI response for any file updates
        process_openai_response(assistant_reply)

    except Exception as e:
        print("An error occurred while communicating with OpenAI:", e)

if __name__ == "__main__":
    main()
