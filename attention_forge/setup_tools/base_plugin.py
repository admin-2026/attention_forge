# base_plugin.py

import yaml
import os

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
            file.write("# Configuration file for Attention Forge\n")
            file.write("#\n")
            for key, value in BaseSetupPlugin.context_defaults.items():
                if key in ['include_paths', 'tree_paths', 'ignore_paths']:
                    file.write(f"# {key}:\n")
                    for item in value:
                        file.write(f"# - {item}\n")
                else:
                    file.write(yaml.dump({key: value}, default_flow_style=False))
            file.write("\n")

        print(f"✅ Initialized {BaseSetupPlugin.CONTEXT_FILE} with default values.")

    def create_user_message_file(self):
        if not os.path.exists(BaseSetupPlugin.USER_MESSAGE_FILE):
            with open(BaseSetupPlugin.USER_MESSAGE_FILE, 'w') as f:
                f.write("# You can enter commands here instead of using the command line.\n")
            print(f"✅ Created {BaseSetupPlugin.USER_MESSAGE_FILE} with instructional message.")
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

    def create_api_key_file(self):
        """Create the api-key file if it doesn't exist."""
        if not os.path.exists(self.API_KEY_FILE):
            content = "# Place your API key here"
            with open(self.API_KEY_FILE, 'w') as f:
                f.write(content)
            print(f"✅ Created {self.API_KEY_FILE}.")
        else:
            print(f"ℹ️ {self.API_KEY_FILE} already exists.")

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
            file.write(yaml.dump(config, default_flow_style=False))

        print(f"✅ Initialized {self.PROJECT_FILE} with configuration values.")
        print(f"ℹ️ log_file set to: {config.get('log_file', '')}")
        print(f"ℹ️ user_message_file set to: {config.get('user_message_file', '')}")