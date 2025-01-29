from attention_forge.clients.base_client import BaseClient
from ollama import chat, ChatResponse

class OllamaClient(BaseClient):
    def __init__(self, api_key, model, project_config):
        super().__init__(api_key, model, project_config)
    
    def get_name(self):
        return "ollama"

    def complete_chat(self, role_config, user_message):
        messages = self.construct_messages(role_config, user_message)

        ollama_messages = [{"role": msg["role"], "content": msg["content"]} for msg in messages]

        response: ChatResponse = chat(model=self.model, messages=ollama_messages)

        assistant_reply = response.message.content
        request_data = {"model": self.model, "messages": ollama_messages}

        token_usage = {
            "prompt_tokens": getattr(response, 'usage', {}).get('prompt_tokens', None),
            "completion_tokens": getattr(response, 'usage', {}).get('completion_tokens', None),
            "total_tokens": getattr(response, 'usage', {}).get('total_tokens', None)
        }

        response_data = {"response": assistant_reply, "usage": token_usage}
        return request_data, response_data, assistant_reply