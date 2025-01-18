import sys
from api_key_loader import load_api_key
from config_loader import load_project_config, load_role_config
from openai_client import generate_response
from chat_logger import log_chat

def main():
    # Load configurations and API key
    try:
        project_config = load_project_config()
        role_config = load_role_config()
        api_key = load_api_key()
    except Exception as e:
        print(e)
        sys.exit(1)

    # Get user input
    user_message = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Enter your message: ")

    # Generate response using OpenAI API
    try:
        request_data, response_data, assistant_reply = generate_response(api_key, role_config, user_message)
        print("OpenAI Assistant:", assistant_reply)

        # Log the full chat
        log_chat(project_config["log_file"], request_data, response_data)
    except Exception as e:
        print("An error occurred while communicating with OpenAI:", e)

if __name__ == "__main__":
    main()