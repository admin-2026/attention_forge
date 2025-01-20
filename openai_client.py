import openai

def create_openai_client(api_key):
    """Create an OpenAI client instance with the provided API key."""
    return openai.Client(api_key=api_key)

def generate_response(api_key, project_config, role_config, user_message):
    """Generate a response from OpenAI using the latest API format."""
    model = project_config.get("model", "gpt-4-turbo")

    client = create_openai_client(api_key)  # Initialize client with API key

    messages = [
        {"role": "system", "content": role_config.get("developer_message", "")},
        {"role": "assistant", "content": role_config.get("assistant_message", "")},  # Ensure assistant message is included
        {"role": "user", "content": user_message},
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages
    )

    # Extract response data
    assistant_reply = response.choices[0].message.content
    request_data = {"model": model, "messages": messages}
    
    # Extract token usage correctly (without using `.get()`)
    token_usage = {
        "prompt_tokens": response.usage.prompt_tokens,
        "completion_tokens": response.usage.completion_tokens,
        "total_tokens": response.usage.total_tokens
    }

    response_data = {"response": assistant_reply, "usage": token_usage}

    return request_data, response_data, assistant_reply
