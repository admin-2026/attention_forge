def construct_messages(role_config, user_message, include_assistant=True):
    """Construct messages using role configuration and user input."""
    messages = [
        {"role": "system", "content": role_config.get("developer_message", "")},
        {"role": "user", "content": user_message}
    ]

    if include_assistant:
        messages.insert(1, {"role": "assistant", "content": role_config.get("assistant_message", "")})

    return messages