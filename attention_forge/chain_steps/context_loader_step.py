import os
import yaml
import hashlib
from pathlib import Path
import pathspec
from attention_forge.chain_steps.step import Step

class FileSystemHelper:
    @staticmethod
    def is_dir(path):
        return os.path.isdir(path)

    @staticmethod
    def is_file(path):
        return os.path.isfile(path)

    @staticmethod
    def list_dir(path):
        return os.walk(path)

    @staticmethod
    def read_file(path, encoding='utf-8'):
        with open(path, 'r', encoding=encoding) as f:
            return f.read()
    
    @staticmethod
    def calculate_signature(path):
        file_stats = os.stat(path)
        path_and_stats = f"{path}-{file_stats.st_mtime}-{file_stats.st_size}"
        return hashlib.md5(path_and_stats.encode()).hexdigest()


class ContextLoader(Step):
    CONTEXT_CONFIG_FILE = "attention_forge_context.yaml"

    def __init__(self, api_key_loader, fs_helper=None):
        self.api_key_loader = api_key_loader
        self.loaded_files = {}
        self.file_signatures = {}
        self.fs_helper = fs_helper or FileSystemHelper()
        self.visited_dirs = set()  # For tracking visited directories during tree generation

    def run(self, *args, **kwargs):
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
        return {str(Path(path).resolve()) for path in paths}

    def compile_ignore_patterns(self, ignore_patterns):
        return pathspec.PathSpec.from_lines('gitwildmatch', ignore_patterns)

    def is_path_ignored(self, path, ignore_specs):
        rel_path = os.path.relpath(path)
        return ignore_specs.match_file(rel_path)

    def get_directories_tree(self, directory, ignore_specs):
        if directory in self.visited_dirs:
            print(f"⏩ Already visited: {directory}, skipping to prevent recursion loop.")
            return ""

        tree_repr = []
        base_depth = len(Path(directory).parts)

        for dirpath, dirnames, filenames in self.fs_helper.list_dir(directory):
            self.visited_dirs.add(dirpath)
            if self.is_path_ignored(dirpath, ignore_specs):
                print(f"⏩ Skipping tree generation of ignored directory: {dirpath}")
                dirnames[:] = []  # Clear subdirectories to skip traversal
                continue
            
            # Calculate depth for indentation
            current_depth = len(Path(dirpath).parts) - base_depth

            indent = '    ' * current_depth
            tree_repr.append(f'{indent}{os.path.basename(dirpath)}/')
            
            # Increase the level of indentation for files
            file_indent = '    ' * (current_depth + 1)
            for filename in filenames:
                if not self.is_path_ignored(os.path.join(dirpath, filename), ignore_specs):
                    tree_repr.append(f'{file_indent}{filename}')

        return "\n".join(tree_repr)

    def get_files_from_directory(self, directory, ignore_specs):
        all_files = []

        for root, dirs, files in self.fs_helper.list_dir(directory):
            if self.is_path_ignored(root, ignore_specs):
                print(f"⏩ Skipping traversal of ignored directory: {root}")
                dirs[:] = []  # Clear dirs to skip deeper traversal
                continue

            for file in files:
                file_path = os.path.join(root, file)
                if not self.is_path_ignored(file_path, ignore_specs):
                    # print(f"✅ Loading file: {file_path}")
                    all_files.append(file_path)
                else:
                    print(f"⏩ Ignoring file: {file_path}")
        return all_files

    def load_config_and_ignore_paths(self):
        config = self.load_context_config()

        # Read the flag from the config, default to True if not present
        use_gitignore_for_ignore_paths = config.get("use_gitignore_for_ignore_paths", True)

        include_paths = config.get("include_paths", [])
        tree_paths = config.get("tree_paths", [])
        ignore_patterns = config.get("ignore_paths", [])

        if use_gitignore_for_ignore_paths:
            gitignore_patterns = self.load_gitignore_patterns()
            
            # Append gitignore_patterns to ignore_patterns
            ignore_patterns.extend(gitignore_patterns)

        api_key_files = self.api_key_loader.get_loaded_files()
        
        # Compile ignore patterns using pathspec
        ignore_specs = self.compile_ignore_patterns(ignore_patterns + api_key_files)

        return include_paths, tree_paths, ignore_specs

    def load_gitignore_patterns(self):
        """
        Reads patterns from .gitignore if available and returns them as a list.
        Prints a message if .gitignore is found/not found.
        """
        gitignore_file = '.gitignore'
        if self.fs_helper.is_file(gitignore_file):
            print(f"📄 .gitignore found. Loading ignore patterns from {gitignore_file}")
            gitignore_content = self.fs_helper.read_file(gitignore_file)
            return gitignore_content.splitlines()
        else:
            print("ℹ️ No .gitignore file found.")
            return []

    def load_context(self):
        include_paths, tree_paths, ignore_specs = self.load_config_and_ignore_paths()
        
        if not include_paths and not tree_paths:
            self.handle_no_context_case()

        loading_error = False

        for path in include_paths:
            if not self.load_path_by_type(path, ignore_specs):
                loading_error = True

        for dir_path in tree_paths:
            if not self.load_tree_structure(dir_path, ignore_specs):
                loading_error = True

        if loading_error:
            self.handle_loading_errors()

        return self.loaded_files

    def handle_no_context_case(self):
        print("⚠️ Warning: No context was loaded. The context is empty.")
        proceed_with_empty = input("Do you want to proceed with an empty context? (yes/no): ")
        if proceed_with_empty.lower() != 'yes':
            print("Operation aborted by user.")
            exit(0)

    def load_path_by_type(self, path, ignore_specs):
        abs_path = str(Path(path).resolve())
        
        if self.fs_helper.is_dir(abs_path):
            return self.process_directory(abs_path, ignore_specs)
        elif self.fs_helper.is_file(abs_path):
            return self.process_file(abs_path, ignore_specs)
        else:
            print(f"⚠️ Skipping invalid path: {path}")
            return False

    def process_directory(self, directory, ignore_specs):
        if self.is_path_ignored(directory, ignore_specs):
            print(f"⏩ Ignoring directory: {directory}")
            return True

        files = self.get_files_from_directory(directory, ignore_specs)
        return all(self.process_file(file, ignore_specs) for file in files)

    def process_file(self, file_path, ignore_specs):
        if self.is_path_ignored(file_path, ignore_specs):
            print(f"⏩ Ignoring file: {file_path}")
            return True

        print(f"✅ Loading file: {file_path}")
        try:
            file_signature = self.fs_helper.calculate_signature(file_path)
            if file_path in self.file_signatures and self.file_signatures[file_path] == file_signature:
                print(f"🔁 Skipping already loaded file (up-to-date): {file_path}")
                return True
            
            self.load_file_content(file_path)
        except Exception as e:
            print(f"🚨 Warning: Could not read {file_path}. Error: {e}")
            return False

        return True

    def load_file_content(self, file_path):
        file_content = self.fs_helper.read_file(file_path)
        language = self.detect_language(file_path)
        formatted_content = f"### `{file_path}`\n```{language}\n{file_content}\n```"
        self.loaded_files[file_path] = formatted_content
        self.file_signatures[file_path] = self.fs_helper.calculate_signature(file_path)

    def load_tree_structure(self, dir_path, ignore_specs):
        abs_dir_path = str(Path(dir_path).resolve())
        if not self.fs_helper.is_dir(abs_dir_path) or self.is_path_ignored(dir_path, ignore_specs):
            print(f"⏩ Ignoring directory for tree generation: {dir_path}")
            return True
        
        print(f"📁 Generating tree for directory: {dir_path}")
        tree_structure = self.get_directories_tree(abs_dir_path, ignore_specs)
        self.loaded_files[abs_dir_path] = f"### directory `{abs_dir_path}/` structure: \n```\n{tree_structure}\n```"
        return True

    def handle_loading_errors(self):
        proceed = input("Some files could not be loaded. Do you want to proceed? (yes/no): ")
        if proceed.lower() != 'yes':
            print("Operation aborted by user.")
            exit(0)