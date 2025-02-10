# api_key_creator.py

import os
import yaml
from importlib.resources import files

class APIKeyCreator:
    def __init__(self, client_name):
        self.client_name = client_name
        self.api_keys_dir = files('attention_forge').joinpath('api-keys')
        self.client_key_file = self.api_keys_dir / f"{client_name}-key.yaml"

    def create_api_key_file(self):
        """Create or verify an API key file for the client."""
        # Ensure the api-keys directory exists
        if not self.api_keys_dir.exists():
            print(f"Creating directory: {self.api_keys_dir}")
            os.makedirs(self.api_keys_dir)

        if self.client_key_file.exists():
            choice = input(f"Found existing API key file for client '{self.client_name}'. Do you want to use it? (yes/no): ").strip().lower()
            if choice == "yes":
                print("Exiting: Using the existing API key.")
                return

        # If file wasn't found or not using the existing file, ask for a new API key
        api_key = input(f"Enter the API key for client '{self.client_name}': ").strip()
        if not api_key:
            print("Error: No API key provided. Aborting.")
            return

        # Store the new API key file in the api-keys directory
        new_key_file_content = {
            "client": self.client_name,
            "key": api_key
        }

        with open(self.client_key_file, 'w') as f:
            yaml.dump(new_key_file_content, f, default_flow_style=False)
        
        print(f"✅ Created {self.client_key_file} with the provided API key.")
        return self.client_key_file