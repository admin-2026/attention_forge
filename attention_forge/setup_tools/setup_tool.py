import os
import yaml

BUILD_DIR = 'attention_forge_build'
CONTEXT_FILE = 'attention_forge_context.yaml'
PROJECT_FILE = 'attention_forge_project.yaml'
GITIGNORE_FILE = '.gitignore'

context_defaults = {
    'include_paths': ['./src', './scripts'],
    'tree_paths': ['./'],
    'ignore_paths': ['attention_forge_build/', './.git/', 'api-key']
}

project_defaults = {
    'log_file': 'attention_forge_build/chat_history.log',  # Log file path for chat history
    'model': 'gpt-4o',  # Default model to use. Change as needed
    'api_key_file': 'api-key',  # Path to the API key file
    'user_message_file': 'user_message.txt',  # Path to the user message file
    'client': 'openai',  # Set the client type: openai, ollama, or rbx
    'gateway_base_url': "http://apis.example.com/",  # Base URL for the gateway (used with rbx client)
    'max_tokens': 10000  # Maximum number of tokens (used with rbx client)
}

def create_build_directory():
    """Create the attention_forge_build directory if it doesn't exist."""
    if not os.path.exists(BUILD_DIR):
        os.mkdir(BUILD_DIR)
        print(f"✅ Created directory: {BUILD_DIR}")
    else:
        print(f"ℹ️ Directory already exists: {BUILD_DIR}")

def create_or_update_yaml(file_path, defaults, message, with_comments=True):
    """Create or update a yaml file with given defaults, optionally with comments, prompting the user if exists."""
    if os.path.exists(file_path):
        choice = input(f"{file_path} already exists. Do you want to overwrite it? (yes/no): ").strip().lower()
        if choice != 'yes':
            print(f"ℹ️ Preserving existing {file_path}.")
            return

    with open(file_path, 'w') as file:
        if with_comments:
            file.write("# Configuration file\n")
            file.write("#\n")
        for key, value in defaults.items():
            if with_comments:
                # Add detailed comments for each config item
                if key == 'include_paths':
                    file.write("# Include paths to specify directories/files that should be included explicitly.\n")
                elif key == 'tree_paths':
                    file.write("# Tree paths to specify directory structures to load into context.\n")
                elif key == 'log_file':
                    file.write("# Path to the log file where chat history is saved.\n")
                elif key == 'model':
                    file.write("# Model name to be used by the client.\n")
                elif key == 'api_key_file':
                    file.write("# Path to the file containing the API key.\n")
                elif key == 'user_message_file':
                    file.write("# Path to the file containing user messages.\n")
                elif key == 'client':
                    file.write("# Client type. Options are: openai, ollama, rbx.\n")
                elif key == 'gateway_base_url':
                    file.write("# Base URL for the API gateway (used with rbx client).\n")
                elif key == 'max_tokens':
                    file.write("# Maximum number of tokens allowed (used with rbx client).\n")
            # Comment out include_paths, tree_paths, gateway_base_url, and max_tokens by default for user customization
            if key in ['include_paths', 'tree_paths', 'gateway_base_url', 'max_tokens']:
                if isinstance(value, list):
                    file.write(f"# {key}:\n")
                    for item in value:
                        file.write(f"# - {item}\n")
                else:
                    file.write(f"# {key}: {value}\n")
            else:
                file.write(yaml.dump({key: value}, default_flow_style=False))
        file.write("\n")

    print(f"✅ {message}")

def update_gitignore():
    """Add paths to .gitignore if not already present."""
    lines_to_add = [
        f"{BUILD_DIR}/",
        CONTEXT_FILE,
        PROJECT_FILE,
        "api-key"  # Add api-key to .gitignore
    ]

    existing_lines = []
    if os.path.exists(GITIGNORE_FILE):
        with open(GITIGNORE_FILE, 'r') as file:
            existing_lines = file.readlines()

    with open(GITIGNORE_FILE, 'a') as file:
        for line in lines_to_add:
            if f"{line}\n" not in existing_lines:
                file.write(f"{line}\n")
                print(f"✅ Added {line} to {GITIGNORE_FILE}")
            else:
                print(f"ℹ️ {line} is already in {GITIGNORE_FILE}")

def main():
    """Initialize the project environment for Attention Forge."""
    create_build_directory()
    create_or_update_yaml(CONTEXT_FILE, context_defaults, f"Initialized {CONTEXT_FILE} with default values.")
    create_or_update_yaml(PROJECT_FILE, project_defaults, f"Initialized {PROJECT_FILE} with default values.")
    update_gitignore()
    print("🎉 Project is ready for Attention Forge!")

if __name__ == "__main__":
    main()