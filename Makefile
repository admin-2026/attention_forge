# Find Python interpreter and create virtual environment path
PYTHON := $(shell command -v python3 || command -v python || echo py)
VENV_DIR = venv

# Detect OS (Windows vs Unix)
OS := $(shell uname -s 2>/dev/null || echo Windows)

# Determine the correct pip path
ifeq ($(OS), Windows)
	PIP := $(VENV_DIR)\Scripts\pip
	PYTHON_ENV := $(VENV_DIR)\Scripts\python
else
	PIP := $(VENV_DIR)/bin/pip
	PYTHON_ENV := $(VENV_DIR)/bin/python
endif

# Define the default project config file
PROJECT_CONFIG = attention_forge_project.yaml

# Define the developer assistant chain (used for `make run`)
DEV_CHAIN = general_dev

# Define the build directory
BUILD_DIR = .attention_forge

# Check if the project config file exists (Cross-Platform)
ifeq ($(OS), Windows)
	CHECK_PROJECT_CONFIG = if not exist $(PROJECT_CONFIG) ( echo Error: '$(PROJECT_CONFIG)' file not found. Please create the file or specify a valid path. && exit /b 1 )
else
	CHECK_PROJECT_CONFIG = if [ ! -f $(PROJECT_CONFIG) ]; then echo "Error: '$(PROJECT_CONFIG)' file not found."; exit 1; fi
endif

# Create a virtual environment
create-venv: ## Create a virtual environment
	$(PYTHON) -m venv $(VENV_DIR)

# Install dependencies in the virtual environment
install-dependencies: create-venv ## Install required dependencies
	$(PYTHON_ENV) -m pip install --upgrade pip
	$(PYTHON_ENV) -m pip install -r requirements.txt

# Install Attention Forge as a local package in the virtual environment
install: install-dependencies ## Install Attention Forge as a local package
	$(PYTHON_ENV) -m pip install .

# Install Attention Forge in development mode in the virtual environment
dev-install: create-venv ## Install Attention Forge in development mode
	$(PYTHON_ENV) -m pip install -e .

# Uninstall Attention Forge
uninstall: ## Uninstall Attention Forge package
	$(PYTHON_ENV) setup.py clean --all
	$(PYTHON_ENV) -m pip uninstall -y attention_forge

# Run the main script with the developer assistant chain in virtual environment
run: ## Run Attention Forge with the specified default chain
	@$(CHECK_PROJECT_CONFIG)
	$(PYTHON_ENV) attention_forge/main.py $(DEV_CHAIN) $(PROJECT_CONFIG)

# Run the script with a custom chain in virtual environment
run-chain: ## Run Attention Forge with a custom chain (use CHAIN=<chain_name> CONFIG=<config_path>)
	@$(CHECK_PROJECT_CONFIG)
	@if [ -z "$(CHAIN)" ]; then \
		echo "Error: Please specify a chain using CHAIN=<chain_name>"; \
		exit 1; \
	fi
	@if [ -z "$(CONFIG)" ]; then \
		echo "Error: Please specify a config using CONFIG=<config_path>"; \
		exit 1; \
	fi
	$(PYTHON_ENV) attention_forge/main.py $(CHAIN) $(CONFIG)

# Run the script to revert a file from the latest backup
revert: ## Revert a file using the revert chain
	@$(CHECK_PROJECT_CONFIG)
	$(PYTHON_ENV) attention_forge/main.py revert $(PROJECT_CONFIG)

# Check Python formatting with black
format: ## Format code using black
	$(PYTHON_ENV) -m black *.py

# Clean up Python cache files and logs (Cross-Platform)
clean: ## Remove cache files, logs, and backups
ifeq ($(OS), Windows)
	@if exist $(BUILD_DIR)\backup rmdir /S /Q $(BUILD_DIR)\backup 2>nul
	@if exist $(BUILD_DIR)\backup_log.json del /S /Q $(BUILD_DIR)\backup_log.json 2>nul
	@if exist $(BUILD_DIR)\chat_history.log del /S /Q $(BUILD_DIR)\chat_history.log 2>nul
	@if exist *.pyc del /S /Q *.pyc 2>nul
	@if exist __pycache__ rmdir /S /Q __pycache__ 2>nul
else
	@rm -rf $(BUILD_DIR)/backup
	@rm -f $(BUILD_DIR)/backup_log.json
	@rm -f $(BUILD_DIR)/chat_history.log
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -exec rm -rf {} +
endif

# Run unit tests in the virtual environment
test: ## Run unit tests
	$(PYTHON_ENV) -m unittest discover -p "*_test.py"

# Update requirements.txt with current virtual environment packages
update-requirements: ## Update requirements.txt with current installed packages in venv
	$(PYTHON_ENV) -m pip freeze > requirements.txt

# Display help
help:
	@echo ""
	@echo "Available Makefile commands:"
	@echo "  create-venv             - Create a virtual environment"
	@echo "  install                 - Install required dependencies"
	@echo "  install-package         - Install Attention Forge as a local package"
	@echo "  dev-install             - Install Attention Forge in development mode"
	@echo "  uninstall               - Uninstall Attention Forge package"
	@echo "  run                     - Run Attention Forge with the developer assistant role"
	@echo "  run-chain CHAIN=<chain> - Run Attention Forge with a custom chain"
	@echo "  revert                  - Revert a file from the latest backup"
	@echo "  format                  - Format code using black"
	@echo "  clean                   - Remove cache files, logs, and backups"
	@echo "  test                    - Run unit tests"
	@echo "  update-requirements     - Update requirements.txt with current installed packages in venv"
	@echo "  help                    - Show available commands"
	@echo ""