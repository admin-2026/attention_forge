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

### Configuration

1. **API Key**:
   - Place your API key in a file named `api-key` in the project's root directory or specify a different path in `attention_forge_project.yaml`.

2. **Project Configuration**:
   - Edit `attention_forge_project.yaml` to customize settings like logging, model version, and client type.

3. **Role Configuration**:
   - Define roles and their behaviors in YAML files under `role_configs/` and map them in `role_configs/meta.yaml`.

4. **Context Configuration**:
   - Specify files or directories to include/exclude in the context in `attention_forge_context.yaml`.

### Usage

- Run the assistant with the default chain `general_dev`:
  ```bash
  make run
  ```

- Run the assistant with a custom chain:
  ```bash
  make run-chain CHAIN=<chain_name>
  ```
 
- Revert files from the latest backup:
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
- Use "exit" to quit the application or "revert" to restore a file from the latest backup.

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