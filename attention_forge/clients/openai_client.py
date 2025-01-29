from attention_forge.clients.base_client import BaseClient
import openai

class OpenAIClient(BaseClient):
    
    def __init__(self, api_key, model, project_config):
        super().__init__(api_key, model, project_config)
        self.client = openai.Client(api_key=api_key)

    def get_name(self):
        return "openai"

    def complete_chat(self, role_config, user_message):
        messages = self.construct_messages(role_config, user_message)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )

        assistant_reply = response.choices[0].message.content
        request_data = {"model": self.model, "messages": messages}

        token_usage = {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens
        }

        response_data = {"response": assistant_reply, "usage": token_usage}
        return request_data, response_data, assistant_reply