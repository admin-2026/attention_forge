# Attention Forge

Attention Forge is a flexible framework for using AI models such as OpenAI's GPT or custom models to assist with coding tasks, chat interactions, and managing project configurations. It provides functionalities such as role-based assistant behavior, context loading, API key management, and automated backup and update of code files.

## Features

- **Role-Based Assistant**: Define assistant behavior and responses based on roles specified in YAML configuration files.
- **Context Loading**: Load relevant project files and directories to provide context for the assistant.
- **API Key Management**: Securely manage API keys for OpenAI and other clients through configuration files.
- **Logging and Backup**: Log chat history and backup files before updating them based on assistant responses.
- **Makefile Automation**: Use the Makefile for easy installation, running, formatting, cleaning, and role management.
- **Project Initialization**: Quickly set up new projects with default configurations using the `attention-forge-init` command.

## Supported Clients

Attention Forge supports multiple AI clients, each with unique capabilities:

### OpenAI
- **Usage**:
  OpenAI clients are used to interact with models like GPT-4. You can configure it by specifying the `client: "openai"` in your project configuration file. Ensure your API key is correctly set in the `api-key` file or specified path.

### Ollama
- **Usage**:
  Ollama allows you to interact with llm running at your local machine. Set `client: "ollama"` in the configuration.

### RBX
- **Usage**:
  RBX is another supported client, where you specify `client: "rbx"` in the configuration. The RBX client uses custom API endpoints, defined in `gateway_base_url`, to request specific model responses. Ensure `max_tokens` and `model` are set as required.

### DeepSeek
- **Usage**:
  DeepSeek is a newly supported client for advanced conversational AI capabilities. Set `client: "deepseek"` in the configuration. Ensure your API key is correctly positioned in the `api-key` file, and other necessary configurations such as `model` are properly set in `attention_forge_project.yaml`.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- API Key for the selected client (OpenAI, Ollama, or RBX)

### Installation

Install dependencies using the Makefile:

```bash
make install
```

### Using the Init Command

Use the `attention-forge-init` command to initialize a new project environment with default configurations. This command will create necessary configuration files and directories.

```bash
attention-forge-init
```

### Interaction

To start interacte with the LLM, type:

```bash
attention-forge <chain name, default to general_dev>
```

or

```bash
afg <chain name, default to general_dev>
```

Say hello to the LLM.

## Chains

Chains allow you to execute predefined sequences of operations that can involve user input, interactions with AI models, and file management tasks. Here are the currently available chains:

### General Development (`afg general_dev`, default chain, just `afg`)
This chain is designed for development tasks where interactions involve reading user input, consulting an AI model to process the input, and updating files as per the model's suggestions. The chain includes steps to:
- Capture user input via standard input or a specified file.
- Initiate a chat with AI models configured for development interactions.
- Extract responses to update files in the project as needed.

### Revert (`afg revert`)
Designed to manage and revert file updates. This chain focuses on:
- Reverting files to their previous states based on backup logs.
- Presenting user choices for which files to revert, ensuring flexibility and safety in file management.

### Chat (`afg chat`)
This chain provides a streamlined chat interface with an AI model focusing on conversational purposes. It includes:
- Capturing user input.
- Maintaining chats with AI models written as per configuration.

### Configuration

1. **API Key**:
   - Place your API key in a file named `api-key` in the project's root directory or specify a different path in `attention_forge_project.yaml`.

2. **Project Configuration**:
   - Edit `attention_forge_project.yaml` to customize settings like logging, model version, and client type.

3. **Role Configuration**:
   - Define roles and their behaviors in YAML files under `role_configs/` and map them in `role_configs/meta.yaml`.

4. **Context Configuration**:
   - Specify files or directories to include/exclude in the context in `attention_forge_context.yaml`.

## Developement

- Run the assistant with the default chain `general_dev`:
  ```bash
  make run
  ```

- Run the assistant with a custom chain and specify the project configuration (order: chain_name, config_path):
  ```bash
  make run-chain CHAIN=<chain_name> CONFIG=<config_path>
  ```

- Revert files using the revert chain configuration:
  ```bash
  make revert
  ```

- Format code using Black:
  ```bash
  make format
  ```

- Clean cache files and logs:
  ```bash
  make clean
  ```

### Example Commands

- Enter your query or command when prompted by `main.py`.
- Use "exit" to quit the application.

## Directory Structure

- `attention_forge/` - Main source code and modules.
- `role_configs/` - Configuration files for different assistant roles.
- `.attention_forge/` - Directory for logs and backups.

## Plugins

Attention Forge allows users to extend its functionality through plugins. This is useful for adding custom setup steps or initializing additional features.

### Creating a Plugin

1. Create a Python file inside the `attention_forge/setup_tools/plugins` directory.
2. Define a `run()` function that contains the logic for your plugin.

Example:

```python
def run():
    print("This is a custom setup plugin.")
```

### Using Plugins

Plugins are automatically discovered and executed when running the `attention-forge-init` command. Each plugin must define a `run()` function, which will be called during the initialization process.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any new features or bug fixes.

## License

This project is licensed under the MIT License.