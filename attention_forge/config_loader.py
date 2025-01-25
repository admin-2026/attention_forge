import yaml
import os
from importlib.resources import files

# Use importlib.resources to define the role config directory
ROLE_CONFIG_DIR = files('attention_forge').joinpath('role_configs')
META_CONFIG_PATH = ROLE_CONFIG_DIR / "meta.yaml"

# Updated filenames
PROJECT_CONFIG_FILE = "attention_forge_project.yaml"
CONTEXT_CONFIG_FILE = "attention_forge_context.yaml"

def load_config(filename):
    """Load configuration from a YAML file."""
    try:
        with open(filename, "r") as file:
            return yaml.safe_load(file) or {}
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: '{filename}' file not found.")
    except yaml.YAMLError as e:
        raise Exception(f"Error parsing YAML file '{filename}': {e}")

def load_project_config(filepath=PROJECT_CONFIG_FILE):
    """Load Attention Forge project-specific configuration."""
    return load_config(filepath)

def load_context_config():
    """Load Attention Forge context configuration."""
    return load_config(CONTEXT_CONFIG_FILE)
