from attention_forge.chain_steps.step import Step
from attention_forge.chain_steps.chat_logger import ChatLogger

class Chat(Step):
    def __init__(self, api_key, project_config, role_name, role_handler, client, model, chat_logger):
        self.api_key = api_key
        self.project_config = project_config
        self.role_config = None
        self.role_name = role_name
        self.role_handler = role_handler
        self.client = client
        self.model = model
        self.chat_logger = chat_logger

    def run(self, *args):
        user_message = args[0]
        context_files = args[1] if len(args) > 1 else []

        if isinstance(user_message, (list, tuple)):
            user_message = ' '.join(user_message)

        if context_files is None:
            context_files = []

        self.role_config = self.role_handler.initialize_role(self.role_name, context_files)

        # Generate response using the client object with role_config
        self.request_data, self.response_data, self.assistant_reply = self.client.complete_chat(
            self.role_config, user_message
        )

        self.chat_logger.log_chat(self.request_data, self.response_data, self.client.get_name(), self.model)
        self.print_results(self.model)

        return self.response_data

    def print_results(self, model_name):
        client_name = self.client.get_name()
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