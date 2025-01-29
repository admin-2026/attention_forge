import requests
from attention_forge.clients.base_client import BaseClient

class RBXClient(BaseClient):

    def __init__(self, api_key, model, project_config):
        super().__init__(api_key, model, project_config)
        self.headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }

    def get_name(self):
        return "rbx"

    def complete_chat(self, role_config, user_message):
        request_data, response_data, assistant_reply = self._generate_response(role_config, user_message)
        return response_data

    def _generate_response(self, role_config, user_message):
        gateway_base_url = self.project_config.get("gateway_base_url")
        if not gateway_base_url:
            raise ValueError("Gateway base URL not found in project configuration.")

        max_tokens = self.project_config.get("max_tokens")
        if max_tokens is None:
            raise ValueError("Max tokens not found in project configuration.")

        messages = self.construct_messages(role_config, user_message)

        rbx_messages = [{"role": msg["role"], "content": msg["content"]} for msg in messages]

        response = self._perform_request(gateway_base_url, rbx_messages)

        assistant_reply = response["choices"][0]["message"]["content"]
        request_data = {"model": self.model, "messages": rbx_messages}

        token_usage = response.get("usage", {})

        response_data = {"response": assistant_reply, "usage": token_usage}

        return request_data, response_data, assistant_reply

    def _perform_request(self, gateway_base_url, messages):
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": self.project_config.get("max_tokens"),
            "stream": False
        }
        response = requests.post(gateway_base_url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()