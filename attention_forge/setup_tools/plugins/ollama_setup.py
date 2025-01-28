import subprocess
import ollama
import yaml
import os

PROJECT_FILE = 'attention_forge_project.yaml'
DEFAULT_MODEL = "deepseek-r1:8b"
API_KEY_FILE = 'api-key'

class ModelChecker:
    def __init__(self):
        self.pulled_models = self.get_pulled_models()

    def get_pulled_models(self):
        """Retrieve a list of models currently pulled by Ollama."""
        try:
            result = ollama.list()
            models = [model.model for model in result.models]
            return models
        except Exception as e:
            print(f"Error: Unable to retrieve the list of pulled models. {str(e)}")
            return []

    def select_model(self):
        """Allow the user to select a model, providing options to pull the default model if necessary."""
        if not self.pulled_models:
            print(f"No models currently pulled. Default model is '{DEFAULT_MODEL}'.")
            choice = input(f"Do you want to pull and use the default model '{DEFAULT_MODEL}'? (yes/no): ").strip().lower()
            if choice == 'yes':
                self.pull_model(DEFAULT_MODEL)
                return DEFAULT_MODEL
            else:
                return None

        print("Pulled models:")
        for index, model in enumerate(self.pulled_models, start=1):
            print(f"{index}. {model}")

        if DEFAULT_MODEL not in self.pulled_models:
            print(f"0. Pull and use the default model '{DEFAULT_MODEL}'")

        selection = input("Select the number of the model you want to use as the model: ").strip()

        if selection.isdigit():
            index = int(selection)
            if index == 0:
                print("Pulling... It takes a while to pull the model...")
                self.pull_model(DEFAULT_MODEL)
                return DEFAULT_MODEL
            elif 1 <= index <= len(self.pulled_models):
                return self.pulled_models[index - 1]
            else:
                print("Invalid selection.")
                return None
        else:
            print("Invalid input.")
            return None

    def pull_model(self, model_name):
        """Pull a model specified by the user using the ollama API."""
        try:
            ollama.pull(model_name)
            print(f"✅ Successfully pulled model: {model_name}")
        except Exception as e:
            print(f"Error: Failed to pull model '{model_name}'. {str(e)}")

def get_client():
    """Return the client this setup is for."""
    return "ollama"

def check_ollama_installed():
    """Check if Ollama is installed."""
    try:
        subprocess.run(["ollama", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("✅ Ollama is installed.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Ollama is not installed. Please install it before proceeding.")
        exit(1)

def create_dummy_api_key():
    """Create a dummy api-key file with the message 'not used' if it doesn't exist."""
    if not os.path.exists(API_KEY_FILE):
        with open(API_KEY_FILE, 'w') as f:
            f.write("not used")
        print(f"✅ Created dummy {API_KEY_FILE} with message 'not used'.")
    else:
        print(f"ℹ️ {API_KEY_FILE} already exists.")

def generate_project_config():
    """Run the setup specific to Ollama, including installation checks."""
    try:
        check_ollama_installed()
        model_checker = ModelChecker()
        model = model_checker.select_model()

        # Create a dummy API key file
        create_dummy_api_key()

        # Default configurations
        config = {
            'api_key_file': API_KEY_FILE,
            'client': 'ollama',
            'model': model if model else DEFAULT_MODEL,
            'base_client': 'ollama',
            'base_model': model if model else DEFAULT_MODEL,
            'log_file': '.attention_forge/chat_history.log',
            'user_message_file': 'user_message.txt'
        }

        # Write to the project YAML file
        if not os.path.exists(PROJECT_FILE) or input(f"{PROJECT_FILE} already exists. Do you want to overwrite it? (yes/no): ").strip().lower() == 'yes':
            with open(PROJECT_FILE, 'w') as file:
                file.write(yaml.dump(config, default_flow_style=False))
            print(f"✅ Initialized {PROJECT_FILE} with values.")
            print(f"ℹ️ log_file set to: {config['log_file']}")
            print(f"ℹ️ user_message_file set to: {config['user_message_file']}")

        return True
    except Exception as e:
        print(f"❌ Error in Ollama setup: {str(e)}")
        return False