import os
import importlib
from attention_forge.clients.base_client import BaseClient
from attention_forge.chain_steps.chat import Chat
from attention_forge.chain_steps.chat_logger import ChatLogger

class ChatBuilder:
    def __init__(self, api_key, role_handler, project_config):
        self.api_key = api_key
        self.role_handler = role_handler
        self.project_config = project_config
        self.chat_logger = ChatLogger(self.project_config.get("log_file", "chat_log.txt"))
        
        # Discover and load client classes
        self.client_map = self.load_clients()

    def load_clients(self):
        client_map = {}
        client_dir = os.path.dirname(os.path.dirname(__file__)) + "/clients"
        
        for file in os.listdir(client_dir):
            if file.endswith(".py") and file != "__init__.py":
                module_name = f"attention_forge.clients.{file[:-3]}"
                module = importlib.import_module(module_name)
                
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    # Ensure the class is a subclass of BaseClient and is not BaseClient itself
                    if isinstance(attr, type) and issubclass(attr, BaseClient) and attr is not BaseClient:
                        client_instance = attr(self.api_key, None, self.project_config)
                        client_map[client_instance.get_name().lower()] = attr
        
        return client_map

    def build(self, role_name, step_config):
        client_value = step_config.get("client", self.project_config.get("client", "openai"))
        if client_value == "base_client":
            client_name = self.project_config.get("base_client", None)
            if not client_name:
                print("Error: 'base_client' is not defined in the project configuration.")
                sys.exit(1)
        else:
            client_name = client_value

        model_value = step_config.get("model", self.project_config.get("model", ""))
        model = self.project_config.get("base_model", model_value) if model_value == "base_model" else model_value

        # Select the appropriate client class
        client_class = self.client_map.get(client_name)
        if not client_class:
            print(f"Error: Client '{client_name}' is not recognized.")
            sys.exit(1)

        client = client_class(self.api_key, model, self.project_config)

        return Chat(
            self.api_key,
            self.project_config,
            role_name,
            self.role_handler,
            client,
            model,
            self.chat_logger
        )