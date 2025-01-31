import os
import yaml
from importlib.resources import files

class ApiKeyLoader:
    def __init__(self, api_keys_dir='api-keys', additional_api_key_file=None):
        """
        Initialize the ApiKeyLoader by scanning the api_keys directory.
        Accepts an additional API key file for loading.
        """
        # Calculate full path relative to the package path
        self.api_keys_dir = files('attention_forge').joinpath(api_keys_dir)
        self.api_key_map = {}
        self.loaded_files = []  # List to keep track of loaded API key files
        self.preload_api_keys()

        # Load additional API key if provided
        if additional_api_key_file:
            self.load_api_key_file(additional_api_key_file)

    def preload_api_keys(self):
        """Preload all API keys from YAML files in the api_keys directory."""
        # Check if path exists, throw exception if not
        if not self.api_keys_dir.exists():
            raise FileNotFoundError(f"Error: API keys directory '{self.api_keys_dir}' does not exist.")

        # Iterate over all YAML files in the api_keys directory
        for file in self.api_keys_dir.iterdir():
            if file.suffix == '.yaml':
                self.load_api_key_file(file)

    def load_api_key_file(self, file_path):
        """Load API keys from a specified YAML file."""
        with open(file_path, "r") as config_file:
            try:
                key_config = yaml.safe_load(config_file)
                if key_config:
                    client_name = key_config.get("client")
                    api_key = key_config.get("key")
                    if client_name and api_key:
                        self.api_key_map[client_name] = api_key
                # Track the loaded file path
                self.loaded_files.append(str(file_path))
            except yaml.YAMLError as e:
                print(f"Warning: Failed to parse {file_path}: {e}")

    def get_api_key(self, client_name):
        """Return the API key for the given client name. Show warning if not found."""
        if client_name not in self.api_key_map:
            print(f"Warning: API key for client '{client_name}' not found.")
            return ""
        return self.api_key_map[client_name]

    def get_loaded_files(self):
        """Return the list of all loaded API key files."""
        return self.loaded_files

# Example usage
# api_key_loader = ApiKeyLoader('api-keys', 'additional-api-key.yaml')
# api_key = api_key_loader.get_api_key("deepseek")
# loaded_files = api_key_loader.get_loaded_files()