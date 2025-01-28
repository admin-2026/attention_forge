import yaml
import pkg_resources

class Role:
    def __init__(self):
        # Load the meta configuration file at construction.
        self.meta_config = self.load_meta_config()
        self.role_configs = {}
        self.preload_role_configs()

    def load_meta_config(self):
        try:
            # Load the meta.yaml file from the package data
            meta_data = pkg_resources.resource_string(__name__, "role_configs/meta.yaml")
            return yaml.safe_load(meta_data)
        except FileNotFoundError:
            raise FileNotFoundError("Meta configuration file not found.")
        except yaml.YAMLError as e:
            raise Exception(f"Error parsing meta configuration: {e}")

    def preload_role_configs(self):
        # Retrieve and load all role config files specified in meta.yaml
        for role_name, config_file in self.meta_config["roles"].items():
            config_data = pkg_resources.resource_string(__name__, f"role_configs/{config_file}")
            self.role_configs[role_name] = yaml.safe_load(config_data)

    def initialize_role(self, role_name, context_files):
        if role_name not in self.role_configs:
            raise ValueError(f"Role '{role_name}' not found in meta configuration.")

        context_text = "\n".join(context_files.values()) if context_files else ""
        role_config = self.role_configs[role_name]
        role_config["developer_message"] += f"\n\nHere are some relevant code files:\n\n{context_text}"
        return role_config