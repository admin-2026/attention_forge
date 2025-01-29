import yaml
import importlib.resources as pkg_resources
import os

class Role:
    def __init__(self):
        # Initialize role configs by scanning the role_configs directory
        self.role_configs = {}
        self.preload_role_configs()

    def preload_role_configs(self):
        # Directory path for role_configs
        role_configs_dir = pkg_resources.files(__package__).joinpath("role_configs")
        
        # Iterate over all YAML files in the role_configs directory
        for file in os.listdir(role_configs_dir):
            if file.endswith(".yaml"):
                file_path = role_configs_dir.joinpath(file)
                with file_path.open("r") as config_file:
                    role_config = yaml.safe_load(config_file)
                    role_name = role_config.get("name")
                    if role_name:
                        self.role_configs[role_name] = role_config

    def initialize_role(self, role_name, context_files):
        if role_name not in self.role_configs:
            raise ValueError(f"Role '{role_name}' not found.")

        context_text = "\n".join(context_files.values()) if context_files else ""
        role_config = self.role_configs[role_name]
        role_config["developer_message"] += f"\n\nHere are some relevant code files:\n\n{context_text}"
        return role_config