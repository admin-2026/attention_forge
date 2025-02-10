from attention_forge.setup_tools.api_key_creator import APIKeyCreator
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
        'ignore_paths': ['.attention_forge/', './.git/', 'api-key', 'venv/'],
        'use_gitignore_for_ignore_paths': True
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
                    file.write("# Follows the .gitignore style, typically including build artifacts, caches, binaries, etc.\n")
                elif key == 'use_gitignore_for_ignore_paths':
                    file.write("# Use .gitignore for Ignore Paths:\n")
                    file.write("# This option allows the loading mechanism to fetch exclude paths defined in .gitignore.\n")

                file.write("\n")
                if isinstance(value, list):
                    file.write(f"# {key}:\n")
                    for item in value:
                        file.write(f"# - {item}\n")
                else:
                    file.write(f"{key}: {value}\n")

        print(f"✅ Initialized {BaseSetupPlugin.CONTEXT_FILE} with default values.")

    def create_user_message_file(self):
        if not os.path.exists(BaseSetupPlugin.USER_MESSAGE_FILE):
            with open(BaseSetupPlugin.USER_MESSAGE_FILE, 'w') as f:
                pass
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
        
        # Utilize the APIKeyCreator to handle the API key logic
        api_key_creator = APIKeyCreator(client_name)
        api_key_file_path = api_key_creator.create_api_key_file()
        
        if not api_key_file_path:
            print("Error: API key file creation aborted.")
            return

        # Update the project configuration to have the new api-key-file entry
        project_config['api-key-file'] = str(api_key_file_path)
        print(f"ℹ️ Updated project configuration with 'api-key-file': {api_key_file_path}")

    def generate_project_config(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def update_project_yaml(self, config):
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