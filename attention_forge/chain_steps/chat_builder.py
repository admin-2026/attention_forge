from attention_forge.chain_steps.chat import Chat
from attention_forge.chain_steps.chat_logger import ChatLogger
import sys

class ChatBuilder:
    def __init__(self, api_key, role_handler, project_config):
        self.api_key = api_key
        self.role_handler = role_handler
        self.project_config = project_config
        self.chat_logger = ChatLogger(self.project_config.get("log_file", "chat_log.txt"))

    def build(self, role_name, step_config):
        client_value = step_config.get("client", self.project_config.get("client", "openai"))
        if client_value == "base_client":
            if "base_client" in self.project_config:
                client = self.project_config["base_client"]
            else:
                print("Error: 'base_client' is not defined in the project configuration.")
                sys.exit(1)
        else:
            client = client_value

        model_value = step_config.get("model", self.project_config.get("model", ""))
        if model_value == "base_model":
            if "base_model" in self.project_config:
                model = self.project_config["base_model"]
            else:
                print("Error: 'base_model' is not defined in the project configuration.")
                sys.exit(1)
        else:
            model = model_value

        return Chat(
            self.api_key,
            self.project_config,
            role_name,
            self.role_handler,
            client,
            model,
            self.chat_logger
        )