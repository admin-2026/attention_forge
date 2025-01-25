import os
import yaml
from attention_forge.chain_steps.chat_builder import ChatBuilder
from attention_forge.chain_steps.user_input_handler import UserInputHandler

class Chain:
    def __init__(self, chain_name, api_key, role_handler, context_files, project_config):
        self.chain_name = chain_name
        self.chain_dir = os.path.join(os.path.dirname(__file__), "chain_configs")
        self.chain_file_path = os.path.join(self.chain_dir, f"{self.chain_name}.yaml")

        if not os.path.isfile(self.chain_file_path):
            raise FileNotFoundError(f"Chain file '{self.chain_file_path}' not found.")

        self.steps = self.load_chain_config()
        self.chat_builder = ChatBuilder(api_key, role_handler, context_files, project_config)
        self.project_config = project_config
        self.objects_list = self.create_objects_from_steps()

    def load_chain_config(self):
        with open(self.chain_file_path, 'r') as file:
            config = yaml.safe_load(file)
        return config.get("steps", [])

    def create_objects_from_steps(self):
        objects = []
        for step in self.steps:
            step_type = step.get("type")

            if step_type == "user_input":
                source = step.get("source", "stdin")
                user_input_handler = UserInputHandler(source, self.project_config)
                objects.append(user_input_handler)
            elif step_type == "chat":
                chat_object = self.chat_builder.build(
                    step.get("role_name", "default"),
                    step
                )
                objects.append(chat_object)
            else:
                print(f"Unsupported step type: {step_type}")

        return objects

    def run(self):
        step_data = {}  # Store outputs of steps
        for obj in self.objects_list:
            if isinstance(obj, UserInputHandler):
                user_message = obj.run()
                step_data['user_message'] = user_message
            else:
                # Use user_message as input for the Chat object's run method
                response_data = obj.run(step_data.get('user_message', ""))
                # Save response_data for potential future use
                step_data['chat_response_data'] = response_data