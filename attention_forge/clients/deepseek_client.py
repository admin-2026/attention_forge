import requests
import json
from attention_forge.clients.message_constructor import construct_messages

def generate_deepseek_response(api_key, model, role_config, user_message):
    """Generate a response from DeepSeek using the requests library."""
    
    # Construct the messages without the assistant role
    messages = construct_messages(role_config, user_message, include_assistant=False)

    # Prepare the headers for the request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Prepare the payload for the request
    payload = {
        "model": model,
        "messages": messages,
        "stream": False
    }

    # Send request to the DeepSeek API
    response = requests.post("https://api.deepseek.com/chat/completions", headers=headers, json=payload)
    
    # Raise an error for bad responses
    response.raise_for_status()
    
    # Parse the response JSON
    response_json = response.json()

    # Extract relevant data from the response
    assistant_reply = response_json["choices"][0]["message"]["content"]
    request_data = {"model": model, "messages": messages}

    # Safely handle the absence of token usage information
    token_usage = {
        "prompt_tokens": response_json.get('usage', {}).get('prompt_tokens', None),
        "completion_tokens": response_json.get('usage', {}).get('completion_tokens', None),
        "total_tokens": response_json.get('usage', {}).get('total_tokens', None)
    }

    response_data = {"response": assistant_reply, "usage": token_usage}

    return request_data, response_data, assistant_reply