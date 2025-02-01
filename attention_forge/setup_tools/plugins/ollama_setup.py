import subprocess
import ollama
import yaml
import os

from attention_forge.setup_tools.base_plugin import BaseSetupPlugin

PROJECT_FILE = 'attention_forge_project.yaml'
DEFAULT_MODEL = "deepseek-r1:8b"

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

class OllamaSetupPlugin(BaseSetupPlugin):
    DEFAULT_MODEL = "deepseek-r1:8b"

    @staticmethod
    def get_client():
        return "ollama"

    def check_ollama_installed(self):
        """Check if Ollama is installed."""
        try:
            subprocess.run(["ollama", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("✅ Ollama is installed.")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Ollama is not installed. Please install it before proceeding.")
            exit(1)

    def confirm_ollama_running(self):
        """Ask user to confirm that Ollama is running."""
        confirmation = input("Make sure Ollama is currently running? (yes/no): ").strip().lower()
        if confirmation != 'yes':
            print("❌ Please ensure that Ollama is running before proceeding.")
            exit(1)

    def generate_project_config(self):
        try:
            self.check_ollama_installed()
            self.confirm_ollama_running()
            model_checker = ModelChecker()
            model = model_checker.select_model()

            config = {
                'client': 'ollama',
                'model': model if model else self.DEFAULT_MODEL,
                'base_client': 'ollama',
                'base_model': model if model else self.DEFAULT_MODEL,
                'log_file': '.attention_forge/chat_history.log',
                'user_message_file': 'user_message.txt'
            }

            self.update_project_yaml(config)

            return True
        except Exception as e:
            print(f"❌ Error in Ollama setup: {str(e)}")
            return False