import os
import yaml

class Role:
    def __init__(self):
        # Load the meta configuration file at construction.
        self.meta_config = self.load_meta_config()
        self.role_configs = {}
        self.preload_role_configs()

    def load_meta_config(self):
        try:
            with open(os.path.join("attention_forge", "role_configs", "meta.yaml"), "r") as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundError("Meta configuration file not found.")
        except yaml.YAMLError as e:
            raise Exception(f"Error parsing meta configuration: {e}")

    def preload_role_configs(self):
        roles_dir = os.path.join("attention_forge", "role_configs")
        for role_name, config_file in self.meta_config["roles"].items():
            with open(os.path.join(roles_dir, config_file), "r") as file:
                self.role_configs[role_name] = yaml.safe_load(file)

    def initialize_role(self, role_name, context_files):
        if role_name not in self.role_configs:
            raise ValueError(f"Role '{role_name}' not found in meta configuration.")

        context_text = "\n".join(context_files.values()) if context_files else ""
        role_config = self.role_configs[role_name]
        role_config["developer_message"] += f"\n\nHere are some relevant code files:\n\n{context_text}"
        return role_config