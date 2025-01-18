# Define the Python interpreter (use python3 if available, else python)
PYTHON = py

# Define the name of the API key file
API_KEY_FILE = api-key

# Detect OS (Windows vs Unix)
OS := $(shell uname -s 2>/dev/null || echo Windows)

# Check if the API key file exists (cross-platform)
ifeq ($(OS), Windows)
    CHECK_API_KEY = if not exist $(API_KEY_FILE) ( echo Error: '$(API_KEY_FILE)' file not found. Please create the file and add your OpenAI API key. && exit /b 1 )
else
    CHECK_API_KEY = test -f $(API_KEY_FILE) || { echo "Error: '$(API_KEY_FILE)' file not found. Please create the file and add your OpenAI API key."; exit 1; }
endif

# Install dependencies
install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt || $(PYTHON) -m pip install openai

# Run the main script
run:
	@$(CHECK_API_KEY)
	$(PYTHON) main.py

# Run the script with a custom message
run-message:
	@$(CHECK_API_KEY)
	$(PYTHON) main.py "$(MESSAGE)"

# Check Python formatting with black
format:
	$(PYTHON) -m black *.py

# Clean up Python cache files (Cross-platform)
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
	@echo "  make run          Run the main script (prompts for input)"
	@echo "  make run-message MESSAGE='your message'  Run the script with a message"
	@echo "  make format       Format code using black"
	@echo "  make clean        Remove cache files"
	@echo "  make help         Show available commands"