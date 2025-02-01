from attention_forge.setup_tools.base_plugin import BaseSetupPlugin

class GeneralSetupPlugin(BaseSetupPlugin):

    def prompt_user_for_config(self):
        client = input("Enter the client (e.g., openai, deepseek) (default: 'openai'): ").strip()
        model = input("Enter the model to be used (default: 'gpt-4o'): ").strip()

        client = client if client else 'openai'
        model = model if model else 'gpt-4o'

        return {
            # 'api_key_file': api_key,
            'client': client,
            'model': model,
            'base_client': client,
            'base_model': model,
            'log_file': '.attention_forge/chat_history.log',
            'user_message_file': 'user_message.txt'
        }

    @staticmethod
    def get_client():
        return "general"

    def generate_project_config(self):
        try:
            config = self.prompt_user_for_config()
            self.create_api_key_file()
            self.update_project_yaml(config)
            return True
        except Exception as e:
            print(f"❌ Error in general setup: {str(e)}")
            return False