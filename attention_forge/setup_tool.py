import os
import yaml

BUILD_DIR = 'attention_forge_build'
CONTEXT_FILE = 'attention_forge_context.yaml'
PROJECT_FILE = 'attention_forge_project.yaml'
GITIGNORE_FILE = '.gitignore'

context_defaults = {
    'tree_paths': ['./'],
    'ignore_paths': ['attention_forge_build/', './.git/', 'api-key']
}

project_defaults = {
    'log_file': 'attention_forge_build/chat_history.log',
    'model': 'gpt-4o',
    'api_key_file': 'api-key',
    'user_message_file': 'user_message.txt'
}

def create_build_directory():
    """Create the attention_forge_build directory if it doesn't exist."""
    if not os.path.exists(BUILD_DIR):
        os.mkdir(BUILD_DIR)
        print(f"✅ Created directory: {BUILD_DIR}")
    else:
        print(f"ℹ️ Directory already exists: {BUILD_DIR}")

def create_or_update_yaml(file_path, defaults, message):
    """Create or update a yaml file with given defaults, prompting the user if exists."""
    if os.path.exists(file_path):
        choice = input(f"{file_path} already exists. Do you want to overwrite it? (yes/no): ").strip().lower()
        if choice != 'yes':
            print(f"ℹ️ Preserving existing {file_path}.")
            return

    with open(file_path, 'w') as file:
        yaml.dump(defaults, file, default_flow_style=False)
    print(f"✅ {message}")

def update_gitignore():
    """Add paths to .gitignore if not already present."""
    lines_to_add = [
        f"{BUILD_DIR}/",
        CONTEXT_FILE,
        PROJECT_FILE
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