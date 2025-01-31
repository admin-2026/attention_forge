from attention_forge.clients.base_client import BaseClient
import requests

class DeepSeekClient(BaseClient):
    
    def __init__(self, api_key, model, project_config):
        super().__init__(api_key, model, project_config)
        
    @staticmethod
    def get_name():
        return "deepseek"

    def complete_chat(self, role_config, user_message):
        messages = self.construct_messages(role_config, user_message, include_assistant=False)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False
        }

        response = requests.post("https://api.deepseek.com/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        response_json = response.json()

        assistant_reply = response_json["choices"][0]["message"]["content"]
        request_data = {"model": self.model, "messages": messages}

        token_usage = {
            "prompt_tokens": response_json.get('usage', {}).get('prompt_tokens', None),
            "completion_tokens": response_json.get('usage', {}).get('completion_tokens', None),
            "total_tokens": response_json.get('usage', {}).get('total_tokens', None)
        }

        response_data = {"response": assistant_reply, "usage": token_usage}
        return request_data, response_data, assistant_reply