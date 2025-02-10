import requests
from attention_forge.clients.base_client import BaseClient
import json

class FireworksClient(BaseClient):
    
    def __init__(self, api_key, model, project_config):
        super().__init__(api_key, model, project_config)
        
        # Load max_tokens from the project_config or use the default value
        self.max_tokens = project_config.get('max_tokens', 20480)

    @staticmethod
    def get_name():
        return "fireworks"

    def complete_chat(self, role_config, user_message):
        # Construct messages using the provided utility method
        messages = self.construct_messages(role_config, user_message)
        
        # Define the Fireworks API endpoint
        url = "https://api.fireworks.ai/inference/v1/chat/completions"
        
        # Prepare the headers for the request
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        # Create the payload for the request
        payload = {
            "model": self.model,
            "max_tokens": self.max_tokens,  # Use the configured or default max_tokens
            "top_p": 1,
            "top_k": 40,
            "presence_penalty": 0,
            "frequency_penalty": 0,
            "temperature": 0.6,
            "messages": [{"role": msg["role"], "content": msg["content"]} for msg in messages]
        }
        
        # Send the request to the Fireworks API
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an error for bad responses
        response_json = response.json()
        
        # Extract the assistant's reply from the response
        assistant_reply = response_json["choices"][0]["message"]["content"]
        request_data = {"model": self.model, "messages": messages}

        # Extract token usage if available
        token_usage = {
            "prompt_tokens": response_json.get('usage', {}).get('prompt_tokens', None),
            "completion_tokens": response_json.get('usage', {}).get('completion_tokens', None),
            "total_tokens": response_json.get('usage', {}).get('total_tokens', None)
        }

        response_data = {"response": assistant_reply, "usage": token_usage}
        return request_data, response_data, assistant_reply