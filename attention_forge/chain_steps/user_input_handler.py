from attention_forge.chain_steps.step import Step
import os

class UserInputHandler(Step):
    def __init__(self, source='stdin', project_config=None):
        self.source = source
        self.user_message_file = project_config.get("user_message_file", "user_message.txt") if project_config else "user_message.txt"

    def run(self, *previous_msg):
        user_message = None
        if 'file' in self.source and os.path.isfile(self.user_message_file):
            with open(self.user_message_file, "r", encoding="utf-8") as file:
                user_message = file.read().strip()
                if user_message:
                    print(f"📄 Loaded user message from file: {self.user_message_file}")
                    confirmation = input("Do you want to use this message? (yes/no): ").strip().lower()
                    if confirmation != "yes":
                        user_message = None

        if not user_message and 'stdin' in self.source:
            user_message = input("Enter your message: ").strip()

        if not user_message or user_message.lower() == "exit":
            if user_message.lower() == "exit":
                print("Exiting the program. No request sent to OpenAI.")
                exit(0)

        return user_message