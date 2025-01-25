import ollama  # Import the ollama library

DEFAULT_MODEL = "deepseek-r1:8b"

class ModelChecker:
    def __init__(self):
        self.pulled_models = self.get_pulled_models()

    def get_pulled_models(self):
        """Retrieve a list of models currently pulled by Ollama."""
        try:
            # Use ollama.list() to get the list of models
            result = ollama.list()
            # Extract the model names from the result
            models = [model.model for model in result.models]
            return models
        except Exception as e:
            print(f"Error: Unable to retrieve the list of pulled models. {str(e)}")
            return []

    def select_base_model(self):
        """Allow the user to select a base model, providing options to pull the default model if necessary."""
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

        # Let the user select a model
        selection = input("Select the number of the model you want to use as the base model: ").strip()

        if selection.isdigit():
            index = int(selection)
            if index == 0:
                print("Pulling... It takes a while to pull the model...")
                self.pull_model(DEFAULT_MODEL)
                return DEFAULT_MODEL
            elif 1 <= index <= len(self.pulled_models):
                return self.pulled_models[index - 1]  # Return the selected model
            else:
                print("Invalid selection.")
                return None
        else:
            print("Invalid input.")
            return None

    def pull_model(self, model_name):
        """Pull a model specified by the user using the ollama API."""
        try:
            ollama.pull(model_name)  # Use ollama.pull() to pull the model
            print(f"✅ Successfully pulled model: {model_name}")
        except Exception as e:
            print(f"Error: Failed to pull model '{model_name}'. {str(e)}")