import os
import subprocess
import yaml
import importlib.util
import glob

BUILD_DIR = '.attention_forge'
CONTEXT_FILE = 'attention_forge_context.yaml'
PROJECT_FILE = 'attention_forge_project.yaml'
GITIGNORE_FILE = '.gitignore'
PLUGIN_FOLDER = os.path.join(os.path.dirname(__file__), 'plugins')

context_defaults = {
    'include_paths': ['./src', './scripts'],
    'tree_paths': ['./'],
    'ignore_paths': ['.attention_forge/', './.git/', 'api-key']
}

def create_build_directory():
    if not os.path.exists(BUILD_DIR):
        os.mkdir(BUILD_DIR)
        print(f"✅ Created directory: {BUILD_DIR}")
    else:
        print(f"ℹ️ Directory already exists: {BUILD_DIR}")

def create_context_yaml():
    """Create or update the context YAML file with the default values."""
    if os.path.exists(CONTEXT_FILE):
        choice = input(f"{CONTEXT_FILE} already exists. Do you want to overwrite it? (yes/no): ").strip().lower()
        if choice != 'yes':
            print(f"ℹ️ Preserving existing {CONTEXT_FILE}.")
            return

    with open(CONTEXT_FILE, 'w') as file:
        file.write("# Configuration file for Attention Forge\n")
        file.write("#\n")
        for key, value in context_defaults.items():
            if key in ['include_paths', 'tree_paths', 'ignore_paths']:
                file.write(f"# {key}:\n")
                for item in value:
                    file.write(f"# - {item}\n")
            else:
                file.write(yaml.dump({key: value}, default_flow_style=False))
        file.write("\n")

    print(f"✅ Initialized {CONTEXT_FILE} with default values.")

def create_user_message_file():
    """Create user_message.txt file with a default message."""
    user_message_file = 'user_message.txt'
    if not os.path.exists(user_message_file):
        with open(user_message_file, 'w') as f:
            f.write("# You can enter commands here instead of using the command line.\n")
        print(f"✅ Created {user_message_file} with instructional message.")
    else:
        print(f"ℹ️ {user_message_file} already exists.")

def update_gitignore():
    lines_to_add = [
        f"{BUILD_DIR}/",
        CONTEXT_FILE,
        PROJECT_FILE,
        "api-key",
        "user_message.txt"
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

def load_plugins():
    plugins = {}
    plugin_files = glob.glob(os.path.join(PLUGIN_FOLDER, '*.py'))
    for plugin_file in plugin_files:
        plugin_name = os.path.splitext(os.path.basename(plugin_file))[0]
        try:
            spec = importlib.util.spec_from_file_location(plugin_name, plugin_file)
            plugin_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(plugin_module)
            if hasattr(plugin_module, "get_client") and hasattr(plugin_module, "generate_project_config"):
                client_name = plugin_module.get_client()
                plugins[client_name] = plugin_module
        except Exception as e:
            print(f"Error loading plugin {plugin_name}: {str(e)}")
    return plugins

def main():
    # Load and run plugins before setting up the directory or context files
    plugins = load_plugins()

    client_choice = input(f"Available clients: {', '.join(plugins.keys())}. Select the client for setup: ").strip().lower()
    if client_choice in plugins:
        success = plugins[client_choice].generate_project_config()
        if not success:
            print(f"❌ Plugin '{client_choice}' failed to run successfully. Aborting setup.")
            return
    else:
        print(f"❌ Client '{client_choice}' not recognized. Please ensure it's spelled correctly and try again.")
        return

    print("🎉 Plugin ran successfully. Proceeding with remaining setup.")

    # Now create directory and context file
    create_build_directory()

    # Create context file
    create_context_yaml()

    # Create user_message.txt file
    create_user_message_file()

    # Update .gitignore
    update_gitignore()

    print("🎉 Project is ready for Attention Forge!")

if __name__ == "__main__":
    main()