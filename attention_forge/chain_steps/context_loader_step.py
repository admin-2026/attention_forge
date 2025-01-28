from attention_forge.chain_steps.step import Step
import os
import yaml
import hashlib

class ContextLoader(Step):
    CONTEXT_CONFIG_FILE = "attention_forge_context.yaml"

    def __init__(self, api_key):
        self.api_key = api_key
        self.loaded_files = {}
        self.file_signatures = {}

    def run(self, *args, **kwargs):  # Accept additional parameters
        return self.load_context()

    def load_context_config(self):
        try:
            with open(self.CONTEXT_CONFIG_FILE, "r") as file:
                return yaml.safe_load(file) or {}
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: '{self.CONTEXT_CONFIG_FILE}' file not found.")
        except yaml.YAMLError as e:
            raise Exception(f"Error parsing YAML file '{self.CONTEXT_CONFIG_FILE}': {e}")

    def detect_language(self, file_path):
        extension_map = {
            ".py": "python", ".js": "javascript", ".java": "java", ".cpp": "cpp",
            ".c": "c", ".cs": "csharp", ".html": "html", ".css": "css", ".json": "json",
            ".xml": "xml", ".md": "markdown", ".sh": "bash", ".yaml": "yaml"
        }
        ext = os.path.splitext(file_path)[1]
        return extension_map.get(ext, "plaintext")

    def normalize_paths(self, paths):
        return {os.path.abspath(path.rstrip("/")) for path in paths}

    def is_path_ignored(self, path, ignore_paths):
        abs_path = os.path.abspath(path)
        return any(abs_path.startswith(ignored) for ignored in ignore_paths)

    def get_directories_tree(self, directory, ignore_paths, level=0):
        tree_repr = ""
        for dirpath, dirnames, filenames in os.walk(directory):
            indent = '    ' * level
            abs_dirpath = os.path.abspath(dirpath)

            if self.is_path_ignored(dirpath, ignore_paths):
                print(f"⏩ Skipping tree generation of ignored directory: {dirpath}")
                dirnames[:] = []
                continue

            tree_repr += f'{indent}{os.path.basename(dirpath)}/\n'
            for filename in filenames:
                tree_repr += f'{indent}    {filename}\n'

            level += 1

        return tree_repr

    def get_files_from_directory(self, directory, ignore_paths):
        abs_directory = os.path.abspath(directory)

        if self.is_path_ignored(directory, ignore_paths):
            print(f"⏩ Skipping traversal of ignored directory: {directory}")
            return []

        print(f"📂 Scanning directory: {directory}")
        all_files = []

        for root, dirs, files in os.walk(directory):
            abs_root = os.path.abspath(root)

            if self.is_path_ignored(root, ignore_paths):
                print(f"⏩ Skipping traversal of ignored directory: {root}")
                dirs[:] = []
                continue

            for file in files:
                file_path = os.path.join(root, file)
                if self.is_path_ignored(file_path, ignore_paths):
                    print(f"❌ Ignoring file: {file_path}")
                else:
                    print(f"✅ Loading file: {file_path}")
                    all_files.append(file_path)

        return all_files

    def calculate_signature(self, file_path):
        file_stats = os.stat(file_path)
        path_and_stats = f"{file_path}-{file_stats.st_mtime}-{file_stats.st_size}"
        signature = hashlib.md5(path_and_stats.encode()).hexdigest()
        return signature

    def load_context(self):
        config = self.load_context_config()

        include_paths = config.get("include_paths", [])
        tree_paths = config.get("tree_paths", [])
        ignore_paths = self.normalize_paths(config.get("ignore_paths", []))
        ignore_paths.add(os.path.abspath(self.api_key))

        loading_error = False

        if not include_paths:
            print("ℹ️ No files or directories specified in include_paths. Skipping context loading.")

        if not include_paths and not tree_paths:
            return self.loaded_files

        for path in include_paths:
            abs_path = os.path.abspath(path)

            if os.path.isdir(abs_path):
                if self.is_path_ignored(path, ignore_paths):
                    print(f"❌ Ignoring directory: {path}")
                    continue
                files = self.get_files_from_directory(abs_path, ignore_paths)
            elif os.path.isfile(abs_path):
                if self.is_path_ignored(path, ignore_paths):
                    print(f"❌ Ignoring file: {path}")
                    continue
                print(f"✅ Loading file: {path}")
                files = [abs_path]
            else:
                print(f"⚠️ Skipping invalid path: {path}")
                loading_error = True
                continue

            for file_path in files:
                try:
                    file_signature = self.calculate_signature(file_path)
                    if file_path in self.file_signatures and self.file_signatures[file_path] == file_signature:
                        print(f"🔁 Skipping already loaded file (up-to-date): {file_path}")
                        continue

                    with open(file_path, "r", encoding="utf-8") as f:
                        language = self.detect_language(file_path)
                        file_content = f.read()
                        formatted_content = f"### `{file_path}`\n```{language}\n{file_content}\n```"
                        self.loaded_files[file_path] = formatted_content
                        self.file_signatures[file_path] = file_signature
                except Exception as e:
                    print(f"🚨 Warning: Could not read {file_path}. Error: {e}")
                    loading_error = True

        for dir_path in tree_paths:
            abs_dir_path = os.path.abspath(dir_path)
            if os.path.isdir(abs_dir_path):
                if self.is_path_ignored(dir_path, ignore_paths):
                    print(f"❌ Ignoring directory for tree generation: {dir_path}")
                    continue
                print(f"📁 Generating tree for directory: {dir_path}")
                tree_structure = self.get_directories_tree(abs_dir_path, ignore_paths)
                self.loaded_files[abs_dir_path] = f"### directory `{abs_dir_path}/` structure: \n```\n{tree_structure}\n```"

        if loading_error:
            proceed = input("Some files could not be loaded. Do you want to proceed? (yes/no): ")
            if proceed.lower() != 'yes':
                print("Operation aborted by user.")
                exit(0)

        return self.loaded_files