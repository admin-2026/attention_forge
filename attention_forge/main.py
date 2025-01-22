import sys
import os
import uuid
from attention_forge.api_key_loader import load_api_key
from attention_forge.config_loader import load_project_config, load_role_config
from attention_forge.context_loader import load_context
from attention_forge.chat_logger import log_chat
from attention_forge.response_parser import process_openai_response
from attention_forge.user_input_handler import get_user_message
from attention_forge.file_manager import set_run_id

# Import the clients
from attention_forge.clients.openai_client import generate_response as openai_generate_response
from attention_forge.clients.ollama_client import generate_ollama_response
from attention_forge.clients.rbx_client import RBXClient

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
        role_config = load_role_config(role_name)
        api_key_path = project_config.get("api_key_file", "api-key")
        user_message_file_path = project_config.get("user_message_file", "")
        api_key = load_api_key(api_key_path)
        client_type = project_config.get("client", "openai")  # Retrieve client type
    except Exception as e:
        print(f"Configuration error: {e}")
        sys.exit(1)

    print(f"🆔 Run ID: {run_id}")

    user_message = get_user_message(user_message_file_path)
    context_files = load_context(api_key_path)
    context_text = "\n".join(content for content in context_files.values()) if context_files else ""

    if context_text:
        role_config["developer_message"] += f"\n\nHere are some relevant code files:\n\n{context_text}"

    # Select and use the appropriate client
    try:
        if client_type == "ollama":
            request_data, response_data, assistant_reply = generate_ollama_response(
                api_key, project_config, role_config, user_message
            )
        elif client_type == "rbx":
            rbx_client = RBXClient(api_key)
            request_data, response_data, assistant_reply = rbx_client.generate_response(
                project_config, role_config, user_message
            )
        else:
            request_data, response_data, assistant_reply = openai_generate_response(
                api_key, project_config, role_config, user_message
            )

        print(f"{client_type.capitalize()} Assistant:", assistant_reply)

        token_usage = response_data["usage"]
        print(f"📊 Token Usage - Prompt: {token_usage['prompt_tokens']}, "
              f"Completion: {token_usage['completion_tokens']}, "
              f"Total: {token_usage['total_tokens']}")

        log_chat(project_config["log_file"], request_data, response_data)
        process_openai_response(assistant_reply)

    except Exception as e:
        print("An error occurred while communicating with the client:", e)

if __name__ == "__main__":
    main()