import os

def load_api_key(api_key_path="api-key"):
    """Load OpenAI API key from the specified path, or use default."""
    
    if not os.path.isfile(api_key_path):
        raise FileNotFoundError(f"Error: API key file '{api_key_path}' not found. Please specify a valid path in project_config.yaml.")

    try:
        with open(api_key_path, "r") as key_file:
            return key_file.read().strip()
    except Exception as e:
        raise Exception(f"Error loading API key from '{api_key_path}': {e}")