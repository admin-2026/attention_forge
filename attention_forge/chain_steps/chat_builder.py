from attention_forge.chain_steps.chat import Chat
from attention_forge.chain_steps.chat_logger import ChatLogger

class ChatBuilder:
    def __init__(self, api_key, role_handler, context_files, project_config):
        self.api_key = api_key
        self.role_handler = role_handler
        self.context_files = context_files
        self.project_config = project_config
        self.chat_logger = ChatLogger(self.project_config.get("log_file", "chat_log.txt"))

    def build(self, role_name, user_message, step_config):
        client = step_config.get("client", self.project_config.get("client", "openai"))
        model = step_config.get("model", self.project_config.get("model", ""))

        return Chat(
            self.api_key,
            self.project_config,
            role_name,
            self.role_handler,
            self.context_files,
            user_message,
            client,
            model,
            self.chat_logger
        )