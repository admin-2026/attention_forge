import sys
import os
import uuid
from attention_forge.api_key_loader import load_api_key
from attention_forge.config_loader import load_project_config
from attention_forge.context_loader import load_context
from attention_forge.user_input_handler import get_user_message
from attention_forge.file_manager import set_run_id
from attention_forge.role import Role
from attention_forge.chain import Chain

def main():
    run_id = str(uuid.uuid4())
    set_run_id(run_id)

    project_config_path = sys.argv[1] if len(sys.argv) > 1 else "attention_forge_project.yaml"
    chain_name = sys.argv[2] if len(sys.argv) > 2 else "general_dev"

    if not os.path.isfile(project_config_path):
        print(f"Error: Project config file '{project_config_path}' not found.")
        sys.exit(1)

    try:
        project_config = load_project_config(project_config_path)
        api_key_path = project_config.get("api_key_file", "api-key")
        api_key = load_api_key(api_key_path)
        context_files = load_context(api_key_path)
    except Exception as e:
        print(f"Configuration error: {e}")
        sys.exit(1)

    print(f"🆔 Run ID: {run_id}")

    role_handler = Role()

    # Instantiate the Chain object
    chain = Chain(chain_name, api_key, role_handler, context_files, project_config)

    try:
        chain.run()
    except Exception as e:
        print("An error occurred while executing the chain:", e)

if __name__ == "__main__":
    main()