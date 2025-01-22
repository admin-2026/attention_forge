from ollama import chat, ChatResponse
from attention_forge.message_constructor import construct_messages

def generate_ollama_response(api_key, project_config, role_config, user_message):
    """Generate a response from Ollama using the ossama library."""
    model = project_config.get("model", "ollama-turbo")

    messages = construct_messages(role_config, user_message)

    # Prepare messages for Ollama
    ollama_messages = [{"role": msg["role"], "content": msg["content"]} for msg in messages]

    # Send request to Ollama API
    response: ChatResponse = chat(model=model, messages=ollama_messages)

    # Extract relevant data from the response
    assistant_reply = response.message.content
    request_data = {"model": model, "messages": ollama_messages}

    # Safely handle the absence of token usage information
    token_usage = {
        "prompt_tokens": getattr(response, 'usage', {}).get('prompt_tokens', None),
        "completion_tokens": getattr(response, 'usage', {}).get('completion_tokens', None),
        "total_tokens": getattr(response, 'usage', {}).get('total_tokens', None)
    }

    response_data = {"response": assistant_reply, "usage": token_usage}

    return request_data, response_data, assistant_reply