import abc

class BaseClient(metaclass=abc.ABCMeta):

    def __init__(self, api_key, model, project_config):
        self.api_key = api_key
        self.model = model
        self.project_config = project_config

    @staticmethod
    def construct_messages(role_config, user_message, include_assistant=True):
        """Construct messages using role configuration and user input."""
        messages = [
            {"role": "system", "content": role_config.get("developer_message", "")},
            {"role": "user", "content": user_message}
        ]

        if include_assistant:
            messages.insert(1, {"role": "assistant", "content": role_config.get("assistant_message", "")})

        return messages

    @abc.abstractmethod
    def get_name(self):
        pass

    @abc.abstractmethod
    def complete_chat(self, user_message):
        pass