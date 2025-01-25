import os
import yaml
from attention_forge.chain_steps.chat_builder import ChatBuilder

class Chain:
    def __init__(self, chain_name, api_key, role_handler, context_files, user_message):
        self.chain_name = chain_name
        self.chain_dir = os.path.join(os.path.dirname(__file__), "chain_configs")
        self.chain_file_path = os.path.join(self.chain_dir, f"{self.chain_name}.yaml")

        if not os.path.isfile(self.chain_file_path):
            raise FileNotFoundError(f"Chain file '{self.chain_file_path}' not found.")

        self.steps = self.load_chain_config()
        self.chat_builder = ChatBuilder(api_key, role_handler, context_files, self.load_project_config())
        self.objects_list = self.create_objects_from_steps(user_message)

    def load_project_config(self):
        from attention_forge.config_loader import load_project_config
        project_config_path = "attention_forge_project.yaml"  # Default path
        return load_project_config(project_config_path)

    def load_chain_config(self):
        with open(self.chain_file_path, 'r') as file:
            config = yaml.safe_load(file)
        return config.get("steps", [])

    def create_objects_from_steps(self, user_message):
        objects = []
        for step in self.steps:
            step_type = step.get("type")

            if step_type == "chat":
                step_user_message = step.get("user_message", user_message)  # Use user_message if step doesn't have it
                chat_object = self.chat_builder.build(
                    step.get("role_name", "default"),  # Default role name if not specified
                    step_user_message,                 # Pass user_message to the chat builder
                    step                               # Step config
                )
                objects.append(chat_object)
            else:
                print(f"Unsupported step type: {step_type}")
        return objects

    def run(self):
        for obj in self.objects_list:  # Iterate through the steps
            obj.run()  # Call the run method on each step