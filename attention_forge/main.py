import sys
import os
import uuid

from attention_forge.api_key_loader import ApiKeyLoader
from attention_forge.config_loader import load_project_config
from attention_forge.file_manager import set_run_id
from attention_forge.role import Role
from attention_forge.chain import Chain

def main():
    run_id = str(uuid.uuid4())
    set_run_id(run_id)

    chain_name = sys.argv[1] if len(sys.argv) > 1 else "general_dev"
    project_config_path = sys.argv[2] if len(sys.argv) > 2 else "attention_forge_project.yaml"

    if not os.path.isfile(project_config_path):
        print(f"Error: Project config file '{project_config_path}' not found.")
        sys.exit(1)

    try:
        project_config = load_project_config(project_config_path)
        api_keys_dir = project_config.get("api_keys_dir", "api-keys")
        additional_api_key_file = project_config.get("api_key_file", None)
        
        # Instantiate ApiKeyLoader with additional_api_key_file
        api_key_loader = ApiKeyLoader(api_keys_dir=api_keys_dir, additional_api_key_file=additional_api_key_file)
        # Pass ApiKeyLoader object instead of api_key
    except Exception as e:
        print(f"Configuration error: {e}")
        sys.exit(1)

    print(f"🆔 Run ID: {run_id}")

    role_handler = Role()

    # Pass the api_key_loader instead of api_key
    chain = Chain(chain_name, api_key_loader, role_handler, project_config)

    try:
        chain.run()
    except Exception as e:
        print("An error occurred while executing the chain:", e)

if __name__ == "__main__":
    main()
