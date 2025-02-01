## User Guide for Attention Forge

Welcome to **Attention Forge** - your friendly AI-powered assistant for coding, chat, and project management!

### Getting Started

#### Prerequisites
- **Python 3.8** or higher
- An API Key for your chosen AI client (OpenAI or DeepSeek). Some clients don't need API key (Ollama)

#### Installation

Ready to dive in? Let's get your setup started!

1. **Install**:
  Open your terminal and run:
   ```bash
   git clone https://github.com/admin-2026/attention_forge.git
   cd attention_forge
   make install
   ```

2. **Initialize Your Project**:  
   Create a new project environment with:
   ```bash
   cd YOUR_PROJECT
   attention-forge-init
   ```

### Using Attention Forge

**Provide Context**:
Open the `attention_forge_context.yaml` and provide some context for your conversation. The amount of tokens your LLM can take is probably limited. You don't want to include everything at once. Select your context with care.


**Start Chatting with AI**:
To engage with the AI, use:
  ```bash
  attention-forge
  ```
  or its friendly alias:
  ```bash
  afg
  ```

You can type: `Create unit tests for <A GIVEN CLASS_NAME>`. If you want to carefully polish your prompts, you can also put your prompts in the generated `user_message.txt`.

**Chains**
Execute operations with AI assistance:
  - **General Development**:  
    Default chain, simply run `afg`.
  - **Revert Changes**:  
    Revert updates with `afg revert`. Of course, you can also use `git` to manage your changes.
  - **Chat**:  
    Use `afg chat` for conversation-focused sessions.

---

## Developer Guide for Attention Forge

Welcome, Developer! Dive deep into Attention Forge, where innovation meets AI.

### Project Features

- **Role-Based Assistant**: Customize AI behavior using YAML configuration.
- **Log & Backup**: Maintain history and backups of all interactions and changes.
- **Plugin Magic**: LLM Roles, Clients, API-keys, Setup tools, Chains are all plugins.

### Development Setup

You can use `attention-forge` itself to develop the `attention-foge` and this is the recommended way. Run `attention-forge-init` in the repo to setup the env for your development. 

- **Running the Assistant**:
   - Default chain: 
     ```bash
     make run
     ```
   - Custom chain:
     ```bash
     make run-chain CHAIN=<chain_name> CONFIG=<config_path>
     ```

- **Code Quality**:
   - Format code with Black by running:
     ```bash
     make format
     ```

- **Maintenance**:
   - Clean up cache and logs:
     ```bash
     make clean
     ```

### Contributing

We welcome your improvements! Fork this repository and submit a pull request for new features or bug fixes.

### License

This project is under the MIT License.