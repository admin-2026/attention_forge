import openai
import sys
from config import load_api_key


def main():
    # Load API key from config
    try:
        api_key = load_api_key()
    except Exception as e:
        print(e)
        sys.exit(1)

    # Initialize OpenAI client
    client = openai.OpenAI(api_key=api_key)

    # Get user input from command-line arguments or prompt
    if len(sys.argv) > 1:
        user_message = " ".join(sys.argv[1:])
    else:
        user_message = input("Enter your message: ")

    # Call OpenAI API
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo", messages=[{"role": "user", "content": user_message}]
        )
        assistant_reply = response.choices[0].message.content
        print("OpenAI Assistant:", assistant_reply)
    except Exception as e:
        print("An error occurred while communicating with OpenAI:", e)


if __name__ == "__main__":
    main()
