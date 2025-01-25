import os
import subprocess  # Import subprocess to check for command-line tools
import yaml
import importlib.util
import glob

from attention_forge.setup_tools.model_checker import ModelChecker  # Import the new ModelChecker

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

project_defaults = {
    'log_file': '.attention_forge/chat_history.log',
    'model': 'gpt-4o',
    'api_key_file': 'api-key',
    'user_message_file': 'user_message.txt',
    'client': 'openai',
    'gateway_base_url': "http://apis.example.com/",
    'max_tokens': 10000,
    'base_client': 'ollama',  # Default base client for Attention Forge
    # base_model will be added dynamically
}

def check_ollama_installed():
    """Check if ollama is installed by attempting to run 'ollama --version'."""
    try:
        subprocess.run(["ollama", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("✅ Ollama is installed.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Ollama is not installed. Please install it before proceeding.")
        exit(1)

def create_build_directory():
    """Create the .attention_forge directory if it doesn't exist."""
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

    # Ensure client is set to 'ollama' and model is set to 'base_model'
    defaults['client'] = 'ollama'
    if 'base_model' in defaults:
        defaults['model'] = defaults['base_model']

    with open(file_path, 'w') as file:
        if with_comments:
            file.write("# Configuration file for Attention Forge\n")
            file.write("#\n")
        for key, value in defaults.items():
            if with_comments:
                if key == 'base_client':
                    file.write("# Base client for Attention Forge's internal functions.\n")
                elif key == 'base_model':
                    file.write("# Base model for Attention Forge's internal functions.\n")
                elif key == 'client':
                    file.write("# Client type. Default is ollama. Update to use other clients like openai, rbx.\n")
                elif key == 'model':
                    file.write("# Model name to be used by the client. Default is the base model. Update to use different LLMs.\n")
                elif key == 'include_paths':
                    file.write("# Include paths to specify directories/files that should be included explicitly.\n")
                elif key == 'tree_paths':
                    file.write("# Tree paths to specify directory structures to load into context.\n")
                elif key == 'log_file':
                    file.write("# Path to the log file where chat history is saved.\n")
                elif key == 'api_key_file':
                    file.write("# Path to the file containing the API key.\n")
                elif key == 'user_message_file':
                    file.write("# Path to the file containing user messages.\n")
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

def load_plugins():
    """Load and execute all plugins found in the plugins directory."""
    plugin_files = glob.glob(os.path.join(PLUGIN_FOLDER, '*.py'))
    for plugin_file in plugin_files:
        plugin_name = os.path.splitext(os.path.basename(plugin_file))[0]
        try:
            spec = importlib.util.spec_from_file_location(plugin_name, plugin_file)
            plugin_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(plugin_module)
            if hasattr(plugin_module, "run"):
                plugin_module.run()  # Call the run function of the plugin
        except Exception as e:
            print(f"Error loading plugin {plugin_name}: {str(e)}")

def main():
    """Initialize the project environment for Attention Forge."""
    check_ollama_installed()
    create_build_directory()
    create_or_update_yaml(CONTEXT_FILE, context_defaults, f"Initialized {CONTEXT_FILE} with default values.")

    model_checker = ModelChecker()
    base_model = model_checker.select_base_model()
    project_defaults['base_model'] = base_model

    create_or_update_yaml(PROJECT_FILE, project_defaults, f"Initialized {PROJECT_FILE} with default values.")
    update_gitignore()

    # Load and execute plugins
    load_plugins()

    print("🎉 Project is ready for Attention Forge!")

if __name__ == "__main__":
    main()
