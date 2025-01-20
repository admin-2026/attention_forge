# Define the Python interpreter
PYTHON = py

# Define the default project config file
PROJECT_CONFIG = attention_forge_project.yaml

# Define the default role (used for `make run`)
DEFAULT_ROLE = default

# Define the developer assistant role (used for `make dev`)
DEV_ROLE = developer

# Define the build directory
BUILD_DIR = attention_forge_build

# Detect OS (Windows vs Unix)
OS := $(shell uname -s 2>/dev/null || echo Windows)

# Check if the project config file exists (Cross-Platform)
ifeq ($(OS), Windows)
    CHECK_PROJECT_CONFIG = if not exist $(PROJECT_CONFIG) ( echo Error: '$(PROJECT_CONFIG)' file not found. Please create the file or specify a valid path. && exit /b 1 )
else
    CHECK_PROJECT_CONFIG = if [ ! -f $(PROJECT_CONFIG) ]; then echo "Error: '$(PROJECT_CONFIG)' file not found."; exit 1; fi
endif

# Generate requirements.txt from installed packages
requirements:
	pip freeze > requirements.txt

# Install dependencies
install:  ## Install required dependencies
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt || $(PYTHON) -m pip install openai pyyaml

# Install Attention Forge as a local package
install-package:  ## Install Attention Forge as a local package
	$(PYTHON) -m pip install .

# Uninstall Attention Forge
uninstall:  ## Uninstall Attention Forge package
	$(PYTHON) -m pip uninstall -y attention_forge

# Run the main script with the default role
run:  ## Run Attention Forge with the default role
	@$(CHECK_PROJECT_CONFIG)
	$(PYTHON) attention_forge/main.py $(PROJECT_CONFIG) $(DEFAULT_ROLE)

# Run the main script with the developer assistant role
dev:  ## Run Attention Forge with the developer assistant role
	@$(CHECK_PROJECT_CONFIG)
	$(PYTHON) attention_forge/main.py $(PROJECT_CONFIG) $(DEV_ROLE)

# Run the script with a custom role
run-role:  ## Run Attention Forge with a custom role (use ROLE=<role_name>)
	@$(CHECK_PROJECT_CONFIG)
	@if [ -z "$(ROLE)" ]; then \
		echo "Error: Please specify a role using ROLE=<role_name>"; \
		exit 1; \
	fi
	$(PYTHON) main.py $(PROJECT_CONFIG) $(ROLE)

# Run the script to revert a file from the latest backup
revert:  ## Revert a file from the latest backup
	@$(CHECK_PROJECT_CONFIG)
	$(PYTHON) main.py revert

# Check Python formatting with black
format:  ## Format code using black
	$(PYTHON) -m black *.py

# Clean up Python cache files and logs (Cross-Platform)
clean:  ## Remove cache files, logs, and backups
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

# Display help
help:
	@echo ""
	@echo "Available Makefile commands:"
	@echo "  install              - Install required dependencies"
	@echo "  install-package      - Install Attention Forge as a local package"
	@echo "  uninstall            - Uninstall Attention Forge package"
	@echo "  run                  - Run Attention Forge with the default role"
	@echo "  dev                  - Run Attention Forge with the developer assistant role"
	@echo "  run-role ROLE=<role> - Run Attention Forge with a custom role"
	@echo "  revert               - Revert a file from the latest backup"
	@echo "  format               - Format code using black"
	@echo "  clean                - Remove cache files, logs, and backups"
	@echo "  help                 - Show available commands"
	@echo ""