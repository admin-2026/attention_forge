from attention_forge.step import Step
from attention_forge.clients.openai_client import generate_response as openai_generate_response
from attention_forge.clients.ollama_client import generate_ollama_response
from attention_forge.clients.rbx_client import RBXClient
from attention_forge.chat_logger import ChatLogger  # Import ChatLogger

class Chat(Step):
    def __init__(self, api_key, project_config, role_name, role_handler, context_files, user_message, client, model, chat_logger):
        self.api_key = api_key
        self.project_config = project_config
        self.role_config = role_handler.initialize_role(role_name, context_files)
        self.user_message = user_message
        self.request_data = None
        self.response_data = None
        self.assistant_reply = None
        self.client = client
        self.model = model
        self.chat_logger = chat_logger  # Use passed in ChatLogger

    def run(self):
        if self.client == "ollama":
            self.request_data, self.response_data, self.assistant_reply = generate_ollama_response(
                self.api_key, self.project_config, self.role_config, self.user_message
            )
        elif self.client == "rbx":
            rbx_client = RBXClient(self.api_key)
            self.request_data, self.response_data, self.assistant_reply = rbx_client.generate_response(
                self.project_config, self.role_config, self.user_message
            )
        else:
            self.request_data, self.response_data, self.assistant_reply = openai_generate_response(
                self.api_key, self.project_config, self.role_config, self.user_message
            )

        # Log chat and print results
        self.chat_logger.log_chat(self.request_data, self.response_data, self.client, self.model)
        self.print_results(self.model)

    def print_results(self, model_name):
        client_name = self.project_config.get('client', 'openai')
        print(f"{client_name.capitalize()} Assistant:", self.get_assistant_reply())

        token_usage = self.get_response_data()["usage"]
        print(f"📊 Token Usage - Prompt: {token_usage['prompt_tokens']}, "
              f"Completion: {token_usage['completion_tokens']}, "
              f"Total: {token_usage['total_tokens']}")

    def get_request_data(self):
        return self.request_data

    def get_response_data(self):
        return self.response_data

    def get_assistant_reply(self):
        return self.assistant_reply