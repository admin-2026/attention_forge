# Define the Python interpreter
PYTHON = py

# Define the default project config file
PROJECT_CONFIG = project_config.yaml

# Define the default role (used for `make run`)
DEFAULT_ROLE = default

# Define the developer assistant role (used for `make dev`)
DEV_ROLE = developer

# Detect OS (Windows vs Unix)
OS := $(shell uname -s 2>/dev/null || echo Windows)

# Check if the project config file exists (Cross-Platform)
ifeq ($(OS), Windows)
    CHECK_PROJECT_CONFIG = if not exist $(PROJECT_CONFIG) ( echo Error: '$(PROJECT_CONFIG)' file not found. Please create the file or specify a valid path. && exit /b 1 )
else
    CHECK_PROJECT_CONFIG = if [ ! -f $(PROJECT_CONFIG) ]; then echo "Error: '$(PROJECT_CONFIG)' file not found. Please create the file or specify a valid path."; exit 1; fi
endif

# Install dependencies
install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt || $(PYTHON) -m pip install openai pyyaml

# Run the main script with the default role
run:
	@$(CHECK_PROJECT_CONFIG)
	$(PYTHON) main.py $(PROJECT_CONFIG) $(DEFAULT_ROLE)

# Run the main script with the developer assistant role
dev:
	@$(CHECK_PROJECT_CONFIG)
	$(PYTHON) main.py $(PROJECT_CONFIG) $(DEV_ROLE)

# Run the script with a custom role
run-role:
	@$(CHECK_PROJECT_CONFIG)
	@if [ -z "$(ROLE)" ]; then \
		echo "Error: Please specify a role using ROLE=<role_name>"; \
		exit 1; \
	fi
	$(PYTHON) main.py $(PROJECT_CONFIG) $(ROLE)

# Check Python formatting with black
format:
	$(PYTHON) -m black *.py

# Clean up Python cache files (Cross-Platform)
clean:
ifeq ($(OS), Windows)
	@if exist *.pyc del /S /Q *.pyc 2>nul
	@if exist __pycache__ rmdir /S /Q __pycache__ 2>nul
else
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -exec rm -rf {} +
endif

# Display help
help:
	@echo "Makefile commands:"
	@echo "  make install      Install dependencies"
	@echo "  make run          Run the assistant with the default role"
	@echo "  make dev          Run the assistant with the developer assistant role"
	@echo "  make run-role ROLE=<role_name>  Run the assistant with a custom role"
	@echo "  make format       Format code using black"
	@echo "  make clean        Remove cache files"
	@echo "  make help         Show available commands"
