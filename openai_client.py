import openai

def generate_response(api_key, project_config, role_config, user_message):
    """Calls OpenAI API and returns the request, response, and assistant reply."""

    # Retrieve model from project config
    model = project_config.get("model", "gpt-4-turbo")

    # Extract optional system and assistant messages
    developer_message = role_config.get("developer_message", "")
    assistant_message = role_config.get("assistant_message", "")

    # Prepare messages list
    messages = []
    if developer_message:
        messages.append({"role": "system", "content": developer_message})
    if assistant_message:
        messages.append({"role": "assistant", "content": assistant_message})

    # Add the latest user message
    messages.append({"role": "user", "content": user_message})

    # Prepare request data
    request_data = {
        "model": model,  # Use model from config
        "messages": messages
    }

    # Initialize OpenAI client
    client = openai.OpenAI(api_key=api_key)

    # Call OpenAI API
    response = client.chat.completions.create(**request_data)
    assistant_reply = response.choices[0].message.content

    # Convert response usage to dictionary (for JSON serialization)
    usage_dict = {
        "prompt_tokens": response.usage.prompt_tokens,
        "completion_tokens": response.usage.completion_tokens,
        "total_tokens": response.usage.total_tokens
    } if response.usage else {}

    # Prepare response data
    response_data = {
        "model": response.model,
        "usage": usage_dict,
        "choices": [{"index": choice.index, "message": choice.message.content} for choice in response.choices]
    }

    return request_data, response_data, assistant_reply
