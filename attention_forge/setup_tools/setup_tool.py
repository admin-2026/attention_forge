# setup_tool.py

import importlib
import os

from attention_forge.setup_tools.base_plugin import BaseSetupPlugin

PLUGIN_FOLDER = os.path.join(os.path.dirname(__file__), 'plugins')

def load_plugins():
    plugins = {}
    
    if not os.path.exists(PLUGIN_FOLDER):
        print(f"Error: Plugin folder '{PLUGIN_FOLDER}' does not exist.")
        return plugins
    
    for file in os.listdir(PLUGIN_FOLDER):
        if file.endswith(".py") and file != "__init__.py":
            module_name = f"attention_forge.setup_tools.plugins.{file[:-3]}"
            try:
                module = importlib.import_module(module_name)
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if isinstance(attr, type) and issubclass(attr, BaseSetupPlugin) and attr is not BaseSetupPlugin:
                        has_get_client = hasattr(attr, "get_client")
                        has_generate_project_config = hasattr(attr, "generate_project_config")

                        if has_get_client and has_generate_project_config:
                            client_name = attr.get_client()
                            plugins[client_name] = attr()  # Create an instance
                        else:
                            if not has_get_client:
                                print(f"Warning: '{module_name}' does not have 'get_client' function.")
                            if not has_generate_project_config:
                                print(f"Warning: '{module_name}' does not have 'generate_project_config' function.")
                        
            except Exception as e:
                print(f"Error loading plugin {module_name}: {str(e)}")

    return plugins

def main():
    plugins = load_plugins()

    client_choice = input(f"Available clients: {', '.join(plugins.keys())}. Select the client for setup: ").strip().lower()
    if not client_choice in plugins:
        print(f"❌ Client '{client_choice}' not recognized. Please ensure it's spelled correctly and try again.")
        return

    plugin = plugins[client_choice]

    success = plugins[client_choice].generate_project_config()
    if not success:
        print(f"❌ Plugin '{client_choice}' failed to run successfully. Aborting setup.")
        return

    print("🎉 Plugin ran successfully. Proceeding with remaining setup.")

    plugin.create_build_directory()
    plugin.create_context_yaml()
    plugin.create_user_message_file()
    plugin.update_gitignore()

    print("🎉 Project is ready for Attention Forge!")

if __name__ == "__main__":
    main()