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

def load_meta_config():
    """Load the meta.yaml file that maps role names to role config files."""
    return load_config(META_CONFIG_PATH)

def load_role_config(role_name="default"):
    """Load the role configuration based on the role name specified in meta.yaml."""
    meta_config = load_meta_config()
    role_mapping = meta_config.get("roles", {})

    if role_name not in role_mapping:
        raise ValueError(f"Error: Role '{role_name}' not found in meta.yaml.")

    role_file = role_mapping[role_name]
    role_config_path = ROLE_CONFIG_DIR / role_file

    if not role_config_path.exists():
        raise FileNotFoundError(f"Error: Role config file '{role_config_path}' does not exist.")

    return load_config(role_config_path)