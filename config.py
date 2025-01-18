def load_api_key(filename="api-key"):
    """Load OpenAI API key from a file."""
    try:
        with open(filename, "r") as key_file:
            return key_file.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Error: '{filename}' file not found. Please create a file containing your OpenAI API key."
        )
    except Exception as e:
        raise Exception(f"Error loading API key: {e}")
