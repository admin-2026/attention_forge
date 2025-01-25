from attention_forge.clients.openai_client import generate_response as openai_generate_response
from attention_forge.clients.ollama_client import generate_ollama_response
from attention_forge.clients.rbx_client import RBXClient

class Chat:
    def __init__(self, api_key, project_config, role_name, role_handler, context_files, user_message):
        self.api_key = api_key
        self.project_config = project_config

        # Use role_handler to initialize the role configuration
        self.role_config = role_handler.initialize_role(role_name, context_files)

        self.user_message = user_message
        self.request_data = None
        self.response_data = None
        self.assistant_reply = None

    def run(self):
        client_type = self.project_config.get("client", "openai")
        model_name = self.project_config.get("model", "")

        if client_type == "ollama":
            self.request_data, self.response_data, self.assistant_reply = generate_ollama_response(
                self.api_key, self.project_config, self.role_config, self.user_message
            )
        elif client_type == "rbx":
            rbx_client = RBXClient(self.api_key)
            self.request_data, self.response_data, self.assistant_reply = rbx_client.generate_response(
                self.project_config, self.role_config, self.user_message
            )
        else:
            self.request_data, self.response_data, self.assistant_reply = openai_generate_response(
                self.api_key, self.project_config, self.role_config, self.user_message
            )

    def get_request_data(self):
        return self.request_data

    def get_response_data(self):
        return self.response_data

    def get_assistant_reply(self):
        return self.assistant_reply