import sys
import os
import uuid
import argparse

from attention_forge.api_key_loader import ApiKeyLoader
from attention_forge.config_loader import load_project_config
from attention_forge.file_manager import set_run_id
from attention_forge.role import Role
from attention_forge.chain import Chain
from attention_forge.file_checker import FileChecker

def main():
    parser = argparse.ArgumentParser(
        description="""Run the Attention Forge application.
For more information, please visit the project README at:
https://github.com/admin-2026/attention_forge/"""
    )
    parser.add_argument(
        "chain_name",
        nargs="?",
        default="general_dev",
        help="Name of the chain to execute. Defaults to 'general_dev'."
    )
    parser.add_argument(
        "project_config_path",
        nargs="?",
        default="attention_forge_project.yaml",
        help=("Path to the project config file. Defaults to 'attention_forge_project.yaml'. "
              "Refer to the README for more details.")
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Show version information and exit."
    )
    
    args = parser.parse_args()

    if args.version:
        import importlib.metadata
        try:
            version = importlib.metadata.version('attention-forge')
        except importlib.metadata.PackageNotFoundError:
            version = 'unknown'
        print(f"Attention Forge version {version}")
        sys.exit(0)

    run_id = str(uuid.uuid4())
    set_run_id(run_id)

    # Instantiate and run the file checker
    file_checker = FileChecker(project_file=args.project_config_path)
    file_check_result = file_checker.run()

    if file_check_result['status'] == 'not_initialized':
        sys.exit(1)
    elif file_check_result['status'] == 'error':
        print("Exiting due to initialization error.")
        sys.exit(1)
    # Continue if status is 'exists' or 'initialized'

    if not os.path.isfile(args.project_config_path):
        print(f"Error: Project config file '{args.project_config_path}' not found.")
        sys.exit(1)

    try:
        project_config = load_project_config(args.project_config_path)
        api_keys_dir = project_config.get("api_keys_dir", "api-keys")
        additional_api_key_file = project_config.get("api_key_file", None)
        
        # Instantiate ApiKeyLoader with additional_api_key_file
        api_key_loader = ApiKeyLoader(api_keys_dir=api_keys_dir, additional_api_key_file=additional_api_key_file)
    except Exception as e:
        print(f"Configuration error: {e}")
        sys.exit(1)

    print(f"🆔 Run ID: {run_id}")

    role_handler = Role()

    # Pass the api_key_loader instead of api_key
    chain = Chain(args.chain_name, api_key_loader, role_handler, project_config)

    try:
        chain.run()
    except Exception as e:
        print("An error occurred while executing the chain:", e)

if __name__ == "__main__":
    main()