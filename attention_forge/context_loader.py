import os
import yaml

CONTEXT_CONFIG_FILE = "attention_forge_context.yaml"

def load_context_config():
    """Load context configuration from YAML."""
    try:
        with open(CONTEXT_CONFIG_FILE, "r") as file:
            return yaml.safe_load(file) or {}  # Ensure it returns a dictionary
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: '{CONTEXT_CONFIG_FILE}' file not found.")
    except yaml.YAMLError as e:
        raise Exception(f"Error parsing YAML file '{CONTEXT_CONFIG_FILE}': {e}")

def detect_language(file_path):
    """Detect programming language based on file extension."""
    extension_map = {
        ".py": "python", ".js": "javascript", ".java": "java", ".cpp": "cpp",
        ".c": "c", ".cs": "csharp", ".html": "html", ".css": "css", ".json": "json",
        ".xml": "xml", ".md": "markdown", ".sh": "bash", ".yaml": "yaml"
    }
    ext = os.path.splitext(file_path)[1]
    return extension_map.get(ext, "plaintext")  # Default to plaintext

def normalize_paths(paths):
    """Convert relative paths to absolute paths for accurate comparisons."""
    return {os.path.abspath(path.rstrip("/")) for path in paths}  # Normalize paths

def get_files_from_directory(directory, ignore_paths):
    """Retrieve all files from a directory while fully skipping ignored directories."""
    abs_directory = os.path.abspath(directory)

    # Check if the entire directory is ignored
    if any(abs_directory.startswith(ignored) for ignored in ignore_paths):
        print(f"❌ Skipping traversal of ignored directory: {directory}")
        return []

    print(f"📂 Scanning directory: {directory}")
    all_files = []

    for root, dirs, files in os.walk(directory):
        abs_root = os.path.abspath(root)

        # Check if the current directory (or any of its parent paths) is in ignore list
        if any(abs_root.startswith(ignored) for ignored in ignore_paths):
            print(f"❌ Skipping traversal of ignored directory: {root}")
            dirs[:] = []  # Modify dirs in-place to prevent descending into ignored directories
            continue

        for file in files:
            file_path = os.path.join(root, file)
            abs_file_path = os.path.abspath(file_path)

            if any(abs_file_path.startswith(ignored) for ignored in ignore_paths):
                print(f"❌ Ignoring file: {file_path}")
            else:
                print(f"✅ Loading file: {file_path}")
                all_files.append(file_path)

    return all_files

def load_context(api_key_path):
    """Load file contents while ignoring specified paths, including API key path."""
    config = load_context_config()

    include_paths = config.get("include_paths", [])  # Default to empty list
    ignore_paths = normalize_paths(config.get("ignore_paths", []))  # Convert to absolute paths
    ignore_paths.add(os.path.abspath(api_key_path))  # Ensure API key file is always ignored

    loaded_files = {}
    loading_error = False

    if not include_paths:
        print("ℹ️ No files or directories specified in include_paths. Skipping context loading.")
        return loaded_files  # Return an empty dictionary

    for path in include_paths:
        abs_path = os.path.abspath(path)  # Normalize included path

        if os.path.isdir(abs_path):
            # If it's a directory, check if it's ignored before processing
            if any(abs_path.startswith(ignored) for ignored in ignore_paths):
                print(f"❌ Ignoring directory: {path}")
                continue
            files = get_files_from_directory(abs_path, ignore_paths)
        elif os.path.isfile(abs_path):
            if any(abs_path.startswith(ignored) for ignored in ignore_paths):
                print(f"❌ Ignoring file: {path}")
                continue
            print(f"✅ Loading file: {path}")
            files = [abs_path]
        else:
            print(f"⚠️ Skipping invalid path: {path}")
            continue

        # Read the content of each file
        for file_path in files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    language = detect_language(file_path)  # Detect language
                    file_content = f.read()
                    # Format as a Markdown code block
                    formatted_content = f"### `{file_path}`\n```{language}\n{file_content}\n```"
                    loaded_files[file_path] = formatted_content
            except Exception as e:
                print(f"🚨 Warning: Could not read {file_path}. Error: {e}")
                loading_error = True

    if loading_error:
        # Ask the user if they want to proceed despite errors
        proceed = input("Some files could not be loaded. Do you want to proceed? (yes/no): ")
        if proceed.lower() != 'yes':
            print("Operation aborted by user.")
            exit(0)

    return loaded_files