import yaml
import os

PROJECT_FILE = 'attention_forge_project.yaml'

def prompt_user_for_config():
    """Prompt the user for API key, client, and model information with default values."""
    api_key = input("Enter the API key file path (default: 'api-key'): ").strip()
    client = input("Enter the client (e.g., openai, ollama) (default: 'openai'): ").strip()
    model = input("Enter the model to be used (default: 'gpt-4o'): ").strip()

    # Use defaults if inputs are empty
    api_key = api_key if api_key else 'api-key'
    client = client if client else 'openai'
    model = model if model else 'gpt-4o'

    return {
        'api_key_file': api_key,
        'client': client,
        'model': model,
        'base_client': client,  # Set the same as the chosen client for base_client
        'base_model': model,    # Set the same as the chosen model for base_model
        'log_file': '.attention_forge/chat_history.log', # Default log_file path
        'user_message_file': 'user_message.txt'  # Default user_message_file
    }

def update_project_yaml(config):
    """Update the project YAML with user-provided configuration."""
    if os.path.exists(PROJECT_FILE):
        choice = input(f"{PROJECT_FILE} already exists. Do you want to overwrite it? (yes/no): ").strip().lower()
        if choice != 'yes':
            print(f"ℹ️ Preserving existing {PROJECT_FILE}.")
            return

    with open(PROJECT_FILE, 'w') as file:
        file.write(yaml.dump(config, default_flow_style=False))

    print(f"✅ Initialized {PROJECT_FILE} with user-provided values.")
    print(f"ℹ️ log_file set to: {config['log_file']}")
    print(f"ℹ️ user_message_file set to: {config['user_message_file']}")

def get_client():
    """Return the client this setup is for."""
    return "general"

def generate_project_config():
    """General setup for Attention Forge."""
    try:
        config = prompt_user_for_config()
        update_project_yaml(config)
        return True
    except Exception as e:
        print(f"❌ Error in general setup: {str(e)}")
        return False