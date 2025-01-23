import requests
import json
from attention_forge.message_constructor import construct_messages

class RBXClient:

    def __init__(self, api_key):
        self.headers = {
            "Authorization": api_key,
            "Content-Type": "application/json"
        }

    def generate_response(self, project_config, role_config, user_message):
        """Generate a response from RBX using the specific APIs."""
        # Load necessary configuration
        gateway_base_url = project_config.get("gateway_base_url")
        if not gateway_base_url:
            raise ValueError("Gateway base URL not found in project configuration.")

        model_name = project_config.get("model")
        if not model_name:
            raise ValueError("Model name not found in project configuration.")

        max_tokens = project_config.get("max_tokens")
        if max_tokens is None:
            raise ValueError("Max tokens not found in project configuration.")

        messages = construct_messages(role_config, user_message)

        # Convert messages to the format expected by the RBX API
        rbx_messages = [{"role": msg["role"], "content": msg["content"]} for msg in messages]

        response = self.complete_chat(gateway_base_url, rbx_messages, model_name, max_tokens)

        # Extract relevant information from the response
        assistant_reply = response["choices"][0]["message"]["content"]
        request_data = {"model": model_name, "messages": rbx_messages}

        token_usage = response.get("usage", {})  # safely handle token usage

        response_data = {"response": assistant_reply, "usage": token_usage}

        return request_data, response_data, assistant_reply

    def complete_chat(self, gateway_base_url, messages, model_name, max_tokens):
        payload = {
            "model": model_name,
            "messages": messages,
            "max_tokens": max_tokens,
            "stream": False  # Set to True if you want to stream the response
        }
        response = requests.post(gateway_base_url, headers=self.headers, json=payload)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()