import os
import yaml
from attention_forge.chain_steps.chat_builder import ChatBuilder
from attention_forge.chain_steps.user_input_handler import UserInputHandler
from attention_forge.chain_steps.file_updater import FileUpdater

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
            elif step_type == "file_update":
                file_updater = FileUpdater()
                objects.append((file_updater, step))
            else:
                print(f"Unsupported step type: {step_type}")

        return objects

    def run(self):
        step_data = {}  # Store outputs of steps

        for obj, step in self.objects_list:
            # Fetch the input data for the step if an input key is specified
            input_data_key = step.get('input_data_key')
            input_value = step_data.get(input_data_key) if input_data_key else None

            # Run the step with the input value, and capture the output
            output_data = obj.run(input_value)

            # Store the output in step_data if an output key is specified
            output_data_key = step.get('output_data_key')
            if output_data_key:
                step_data[output_data_key] = output_data