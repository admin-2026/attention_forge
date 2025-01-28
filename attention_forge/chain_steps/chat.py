from attention_forge.chain_steps.step import Step
from attention_forge.clients.openai_client import generate_response as openai_generate_response
from attention_forge.clients.ollama_client import generate_ollama_response
from attention_forge.clients.rbx_client import RBXClient
from attention_forge.clients.deepseek_client import generate_deepseek_response  # Import the DeepSeek client
from attention_forge.chain_steps.chat_logger import ChatLogger

class Chat(Step):
    def __init__(self, api_key, project_config, role_name, role_handler, client, model, chat_logger):
        self.api_key = api_key
        self.project_config = project_config
        self.role_config = None  # Initialize as None
        self.role_name = role_name
        self.role_handler = role_handler
        self.client = client
        self.model = model
        self.chat_logger = chat_logger

    def run(self, *args):
        # Unpack the arguments
        user_message = args[0]
        context_files = args[1] if len(args) > 1 else []

        # Combine user messages into a single string if it's a list or tuple
        if isinstance(user_message, (list, tuple)):
            user_message = ' '.join(user_message)

        # Initialize context_files if it's None
        if context_files is None:
            context_files = []

        # Initialize the role configuration during the run
        self.role_config = self.role_handler.initialize_role(self.role_name, context_files)

        # Selecting the appropriate client to generate a response
        if self.client == "ollama":
            self.request_data, self.response_data, self.assistant_reply = generate_ollama_response(
                self.api_key, self.model, self.role_config, user_message
            )
        elif self.client == "rbx":
            rbx_client = RBXClient(self.api_key)
            self.request_data, self.response_data, self.assistant_reply = rbx_client.generate_response(
                self.model, self.project_config, self.role_config, user_message
            )
        elif self.client == "deepseek":
            self.request_data, self.response_data, self.assistant_reply = generate_deepseek_response(
                self.api_key, self.model, self.role_config, user_message
            )
        else:
            self.request_data, self.response_data, self.assistant_reply = openai_generate_response(
                self.api_key, self.model, self.role_config, user_message
            )

        # Log chat and print results
        self.chat_logger.log_chat(self.request_data, self.response_data, self.client, self.model)
        self.print_results(self.model)

        return self.response_data

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