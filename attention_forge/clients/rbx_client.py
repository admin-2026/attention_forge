import requests
import json
from attention_forge.message_constructor import construct_messages

class RBXClient:
    gateway_base_url = "http://apis.example.com/"

    def __init__(self, api_key):
        self.headers = {
            "Authorization": api_key,
            "Content-Type": "application/json"
        }

    def generate_response(self, project_config, role_config, user_message):
        """Generate a response from RBX using the specific APIs."""
        # Load model name from project config
        model_name = project_config.get("model", "Llama-3.1")

        messages = construct_messages(role_config, user_message)

        # Convert messages to the format expected by the RBX API
        rbx_messages = [{"role": msg["role"], "content": msg["content"]} for msg in messages]

        response = self.complete_chat(rbx_messages)

        # Extract relevant information from the response
        assistant_reply = response["choices"][0]["message"]["content"]
        request_data = {"model": model_name, "messages": rbx_messages}

        token_usage = response.get("usage", {})  # safely handle token usage

        response_data = {"response": assistant_reply, "usage": token_usage}

        return request_data, response_data, assistant_reply

    def complete_chat(self, messages, model_name, max_tokens=10000):
        payload = {
            "model": model_name,
            "messages": messages,
            "max_tokens": max_tokens,
            "stream": False  # Set to True if you want to stream the response
        }
        response = requests.post(self.gateway_base_url, headers=self.headers, json=payload)
        return response.json()