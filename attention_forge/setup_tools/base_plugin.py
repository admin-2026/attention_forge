import yaml
import os
from importlib.resources import files

class BaseSetupPlugin:
    PROJECT_FILE = 'attention_forge_project.yaml'
    BUILD_DIR = '.attention_forge'
    CONTEXT_FILE = 'attention_forge_context.yaml'
    USER_MESSAGE_FILE = 'user_message.txt'
    GITIGNORE_FILE = '.gitignore'
    API_KEY_FILE = 'api-key'

    context_defaults = {
        'include_paths': ['./src', './scripts'],
        'tree_paths': ['./'],
        'ignore_paths': ['.attention_forge/', './.git/', 'api-key']
    }

    def create_build_directory(self):
        if not os.path.exists(BaseSetupPlugin.BUILD_DIR):
            os.mkdir(BaseSetupPlugin.BUILD_DIR)
            print(f"✅ Created directory: {BaseSetupPlugin.BUILD_DIR}")
        else:
            print(f"ℹ️ Directory already exists: {BaseSetupPlugin.BUILD_DIR}")

    def create_context_yaml(self):
        if os.path.exists(BaseSetupPlugin.CONTEXT_FILE):
            choice = input(f"{BaseSetupPlugin.CONTEXT_FILE} already exists. Do you want to overwrite it? (yes/no): ").strip().lower()
            if choice != 'yes':
                print(f"ℹ️ Preserving existing {BaseSetupPlugin.CONTEXT_FILE}.")
                return

        with open(BaseSetupPlugin.CONTEXT_FILE, 'w') as file:
            file.write("# Context Configuration File\n")
            file.write("# This file defines various paths that will be considered during the during the conversation with AI.\n")
            file.write("#\n")
            for key, value in BaseSetupPlugin.context_defaults.items():
                file.write("\n\n")
                if key == 'include_paths':
                    file.write("# Include Paths:\n")
                    file.write("# These are files or directories whose content will be included\n")
                    file.write("# as context when interacting with the AI model.\n")
                elif key == 'tree_paths':
                    file.write("# Tree Paths:\n")
                    file.write("# These are directories whose directory structure (but not the content)\n")
                    file.write("# will be loaded during conversations with the AI model.\n")
                elif key == 'ignore_paths':
                    file.write("# Ignore Paths:\n")
                    file.write("# These are files or directories to be excluded from context loading.\n")
                    file.write("# Typically, you can ignore build artifacts, caches, binaries, etc.\n")

                file.write("\n")
                file.write(f"# {key}:\n")
                for item in value:
                    file.write(f"# - {item}\n")
                
            file.write("\n")

        print(f"✅ Initialized {BaseSetupPlugin.CONTEXT_FILE} with default values.")

    def create_user_message_file(self):
        if not os.path.exists(BaseSetupPlugin.USER_MESSAGE_FILE):
            with open(BaseSetupPlugin.USER_MESSAGE_FILE, 'w') as f:
                pass  # Create the file without writing anything
            print(f"✅ Created {BaseSetupPlugin.USER_MESSAGE_FILE}.")
        else:
            print(f"ℹ️ {BaseSetupPlugin.USER_MESSAGE_FILE} already exists.")

    def update_gitignore(self):
        lines_to_add = [
            f"{BaseSetupPlugin.BUILD_DIR}/",
            BaseSetupPlugin.CONTEXT_FILE,
            BaseSetupPlugin.PROJECT_FILE,
            self.API_KEY_FILE,
            BaseSetupPlugin.USER_MESSAGE_FILE
        ]

        existing_lines = []
        if os.path.exists(BaseSetupPlugin.GITIGNORE_FILE):
            with open(BaseSetupPlugin.GITIGNORE_FILE, 'r') as file:
                existing_lines = file.readlines()

        with open(BaseSetupPlugin.GITIGNORE_FILE, 'a') as file:
            for line in lines_to_add:
                if f"{line}\n" not in existing_lines:
                    file.write(f"{line}\n")
                    print(f"✅ Added {line} to {BaseSetupPlugin.GITIGNORE_FILE}")
                else:
                    print(f"ℹ️ {line} is already in {BaseSetupPlugin.GITIGNORE_FILE}")

    def create_api_key_file(self, project_config):
        """Create or utilize the client-specific api-key file."""
        client_name = project_config.get("client")
        if not client_name:
            print("Error: 'client' not found in project configuration.")
            return

        # Calculate paths
        api_keys_dir = files('attention_forge').joinpath('api-keys')
        client_key_file_in_package = api_keys_dir / f"{client_name}-key.yaml"

        # Ensure the api-keys directory exists
        if not api_keys_dir.exists():
            print(f"Creating directory: {api_keys_dir}")
            os.makedirs(api_keys_dir)

        if client_key_file_in_package.exists():
            choice = input(f"Found existing API key file for client '{client_name}' in the package. Do you want to use it? (yes/no): ").strip().lower()
            if choice == "yes":
                print("Exiting: Using the existing API key.")
                return

        # If file wasn't found or not using the existing file, ask for a new API key
        api_key = input(f"Enter the API key for client '{client_name}': ").strip()
        if not api_key:
            print("Error: No API key provided. Aborting.")
            return

        # Store the new API key file in the api-keys directory within the package
        new_key_file_content = {
            "client": client_name,
            "key": api_key
        }

        with open(client_key_file_in_package, 'w') as f:
            yaml.dump(new_key_file_content, f, default_flow_style=False)
        print(f"✅ Created {client_key_file_in_package} with the provided API key.")

        # Update the project configuration to have the new api-key-file entry
        project_config['api-key-file'] = str(client_key_file_in_package)
        print(f"ℹ️ Updated project configuration with 'api-key-file': {client_key_file_in_package}")

    def generate_project_config(self):
        """Run the setup configuration for the plugin."""
        raise NotImplementedError("Subclasses should implement this method.")

    def update_project_yaml(self, config):
        """Update the project YAML with provided configuration."""
        if os.path.exists(self.PROJECT_FILE):
            choice = input(f"{self.PROJECT_FILE} already exists. Do you want to overwrite it? (yes/no): ").strip().lower()
            if choice != 'yes':
                print(f"ℹ️ Preserving existing {self.PROJECT_FILE}.")
                return

        with open(self.PROJECT_FILE, 'w') as file:
            yaml.dump(config, file, default_flow_style=False)

        print(f"✅ Initialized {self.PROJECT_FILE} with configuration values.")
        print(f"ℹ️ log_file set to: {config.get('log_file', '')}")
        print(f"ℹ️ user_message_file set to: {config.get('user_message_file', '')}")