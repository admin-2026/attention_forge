import yaml

def load_config(filename):
    """Load configuration from a YAML file."""
    try:
        with open(filename, "r") as file:
            config = yaml.safe_load(file)
            return config
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: '{filename}' file not found. Please create a valid YAML config file.")
    except yaml.YAMLError as e:
        raise Exception(f"Error parsing YAML file '{filename}': {e}")

def load_project_config():
    """Load project-specific configuration."""
    return load_config("project_config.yaml")

def load_role_config():
    """Load role-specific configuration."""
    return load_config("role_config.yaml")