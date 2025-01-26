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
            step['input_data_key'] = step.get("input_data_key")
            step['output_data_key'] = step.get("output_data_key")

            if step_type == "user_input":
                source = step.get("source", "stdin")
                user_input_handler = UserInputHandler(source, self.project_config)
                objects.append((user_input_handler, step))
            elif step_type == "chat":
                chat_object = self.chat_builder.build(
                    step.get("role_name", "default"),
                    step
                )
                objects.append((chat_object, step))
            else:
                print(f"Unsupported step type: {step_type}")

        return objects

    def run(self):
        step_data = {}  # Store outputs of steps
        for obj, step in self.objects_list:
            input_data_key = step.get('input_data_key')
            output_data_key = step.get('output_data_key')

            # Determine input to pass to this step
            input_value = step_data.get(input_data_key) if input_data_key else None

            if isinstance(obj, UserInputHandler):
                user_message = obj.run()
                # Store output if output_data_key is provided
                if output_data_key:
                    step_data[output_data_key] = user_message
            else:
                # Use input value for the Chat object's run method
                response_data = obj.run(input_value)
                # Store output if output_data_key is provided
                if output_data_key:
                    step_data[output_data_key] = response_data