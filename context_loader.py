import os
import yaml

def load_context_config(filename="context_config.yaml"):
    """Load context configuration from YAML."""
    try:
        with open(filename, "r") as file:
            return yaml.safe_load(file) or {}  # Ensure it returns a dictionary
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: '{filename}' file not found. Please create a valid YAML config file.")
    except yaml.YAMLError as e:
        raise Exception(f"Error parsing YAML file '{filename}': {e}")

def get_files_from_directory(directory, ignore_paths):
    """Retrieve all files from a directory, ignoring specified paths."""
    all_files = []
    if directory in ignore_paths:
        print(f"❌ Ignoring directory: {directory}")
        return []
    
    print(f"📂 Loading directory: {directory}")
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path in ignore_paths:
                print(f"❌ Ignoring file: {file_path}")
            else:
                print(f"✅ Loading file: {file_path}")
                all_files.append(file_path)
    return all_files

def detect_language(file_path):
    """Detect programming language based on file extension."""
    extension_map = {
        ".py": "python", ".js": "javascript", ".java": "java", ".cpp": "cpp",
        ".c": "c", ".cs": "csharp", ".html": "html", ".css": "css", ".json": "json",
        ".xml": "xml", ".md": "markdown", ".sh": "bash", ".yaml": "yaml"
    }
    ext = os.path.splitext(file_path)[1]
    return extension_map.get(ext, "plaintext")  # Default to plaintext

def load_context():
    """Load file contents from context_config.yaml while ignoring specified paths."""
    config = load_context_config()
    
    include_paths = config.get("include_paths", [])  # Default to empty list
    ignore_paths = set(config.get("ignore_paths", []))  # Default to empty set for fast lookup

    loaded_files = {}

    if not include_paths:
        print("ℹ️ No files or directories specified in include_paths. Skipping context loading.")
        return loaded_files  # Return an empty dictionary

    for path in include_paths:
        if os.path.isdir(path):
            # If it's a directory, get all files (excluding ignored ones)
            files = get_files_from_directory(path, ignore_paths)
        elif os.path.isfile(path):
            if path in ignore_paths:
                print(f"❌ Ignoring file: {path}")
                continue
            print(f"✅ Loading file: {path}")
            files = [path]
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
                    formatted_content = f"### {file_path}:\n```{language}\n{file_content}\n```"
                    loaded_files[file_path] = formatted_content
            except Exception as e:
                print(f"🚨 Warning: Could not read {file_path}. Error: {e}")

    return loaded_files
