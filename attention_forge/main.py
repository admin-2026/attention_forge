import sys
import os
import uuid
from attention_forge.api_key_loader import load_api_key
from attention_forge.config_loader import load_project_config
from attention_forge.context_loader import load_context
from attention_forge.chat_logger import log_chat
from attention_forge.user_input_handler import get_user_message
from attention_forge.file_manager import set_run_id
from attention_forge.chat import Chat
from attention_forge.role import Role  # Import Role

def main():
    run_id = str(uuid.uuid4())
    set_run_id(run_id)

    project_config_path = sys.argv[1] if len(sys.argv) > 1 else "attention_forge_project.yaml"
    role_name = sys.argv[2] if len(sys.argv) > 2 else "default"

    if not os.path.isfile(project_config_path):
        print(f"Error: Project config file '{project_config_path}' not found.")
        sys.exit(1)

    try:
        project_config = load_project_config(project_config_path)
        api_key_path = project_config.get("api_key_file", "api-key")
        user_message_file_path = project_config.get("user_message_file", "")
        api_key = load_api_key(api_key_path)
        model_name = project_config.get("model", "")
    except Exception as e:
        print(f"Configuration error: {e}")
        sys.exit(1)

    print(f"🆔 Run ID: {run_id}")

    user_message = get_user_message(user_message_file_path)
    context_files = load_context(api_key_path)

    # Initialize Role class and prepare role config
    role_handler = Role()

    # Initialize Chat class with role_name, role_handler, and context_files
    chat = Chat(api_key, project_config, role_name, role_handler, context_files, user_message)

    try:
        chat.run()
        assistant_reply = chat.get_assistant_reply()
        request_data = chat.get_request_data()
        response_data = chat.get_response_data()

        print(f"{project_config.get('client', 'openai').capitalize()} Assistant:", assistant_reply)

        token_usage = response_data["usage"]
        print(f"📊 Token Usage - Prompt: {token_usage['prompt_tokens']}, "
              f"Completion: {token_usage['completion_tokens']}, "
              f"Total: {token_usage['total_tokens']}")

        log_chat(project_config["log_file"], request_data, response_data, project_config.get("client", "openai"), model_name)

    except Exception as e:
        print("An error occurred while communicating with the client:", e)

if __name__ == "__main__":
    main()