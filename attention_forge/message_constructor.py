def construct_messages(role_config, user_message):
    """Construct messages using role configuration and user input."""
    return [
        {"role": "system", "content": role_config.get("developer_message", "")},
        {"role": "assistant", "content": role_config.get("assistant_message", "")},
        {"role": "user", "content": user_message},
    ]