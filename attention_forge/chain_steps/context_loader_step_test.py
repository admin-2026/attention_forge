import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path
import os
from attention_forge.chain_steps.context_loader_step import ContextLoader, FileSystemHelper

class TestContextLoader(unittest.TestCase):
    def setUp(self):
        # Mock the API Key Loader
        self.mock_api_key_loader = MagicMock()
        self.mock_api_key_loader.get_loaded_files.return_value = []

        # Initialize the ContextLoader with the mocked api_key_loader
        self.context_loader = ContextLoader(api_key_loader=self.mock_api_key_loader)

        # Mock the file system helper
        self.fs_helper_mock = patch('attention_forge.chain_steps.context_loader_step.FileSystemHelper', autospec=True).start()
        self.addCleanup(patch.stopall)

    # Existing tests ...

    def test_load_context_config_file_not_found(self):
        with patch('builtins.open', side_effect=FileNotFoundError):
            with self.assertRaises(FileNotFoundError):
                self.context_loader.load_context_config()

    def test_detect_language(self):
        self.assertEqual(self.context_loader.detect_language("file.py"), "python")
        self.assertEqual(self.context_loader.detect_language("file.js"), "javascript")
        self.assertEqual(self.context_loader.detect_language("file.unknown"), "plaintext")

    def test_normalize_paths(self):
        paths = ["./file.txt", "../parent/file.txt"]
        expected_normalized = {str(Path(p).resolve()) for p in paths}
        self.assertEqual(self.context_loader.normalize_paths(paths), expected_normalized)

    def test_is_path_ignored(self):
        ignore_paths = self.context_loader.normalize_paths(["ignored_path"])
        self.assertTrue(self.context_loader.is_path_ignored("ignored_path/file.txt", ignore_paths))
        self.assertFalse(self.context_loader.is_path_ignored("included_path/file.txt", ignore_paths))

    def test_get_files_from_directory(self):
        directory = "/test_dir"

        # Define different directory structures to return
        dir_structure_1 = [
            (directory, ("subdir",), ("file1.txt", "file2.py")),
        ]

        dir_structure_2 = [
            (os.path.join(directory, "subdir"), (), ("file3.js",)),
        ]

        # Use side_effect to simulate different states of the directory structure
        self.fs_helper_mock.list_dir.side_effect = [dir_structure_1, dir_structure_2]

        ignore_paths = set()
        expected_files = [
            os.path.join(directory, "file1.txt"),
            os.path.join(directory, "file2.py"),
            os.path.join(directory, "subdir", "file3.js"),
        ]

        # Create an instance with the mocked file system helper
        context_loader = ContextLoader(api_key_loader=self.mock_api_key_loader, fs_helper=self.fs_helper_mock)

        # Act
        files = context_loader.get_files_from_directory(directory, ignore_paths)

        # Assert
        self.assertEqual(sorted(files), sorted(expected_files))

    def test_get_files_from_directory_with_ignored_paths(self):
        directory = "/test_dir"
        
        # Define a directory structure
        dir_structure_1 = [
            (directory, ("subdir",), ("file1.txt", "file2.py")),
        ]

        dir_structure_2 = [
            (os.path.join(directory, "subdir"), (), ("file3.js",)),
        ]

        # Use side_effect to simulate different states of the directory structure
        self.fs_helper_mock.list_dir.side_effect = [dir_structure_1, dir_structure_2]

        # Define ignored paths
        ignore_paths = self.context_loader.normalize_paths(["/test_dir/subdir"])

        # Create an instance with the mocked file system helper
        context_loader = ContextLoader(api_key_loader=self.mock_api_key_loader, fs_helper=self.fs_helper_mock)

        # Act
        files = context_loader.get_files_from_directory(directory, ignore_paths)

        # The ignored directory should not have its files listed
        expected_files = [
            os.path.join(directory, "file1.txt"),
            os.path.join(directory, "file2.py"),
        ]

        # Assert
        self.assertEqual(sorted(files), sorted(expected_files))

    def test_process_file(self):
        fake_file = "/test_dir/file.txt"
        
        # Mocking
        self.fs_helper_mock.is_file.return_value = True
        self.fs_helper_mock.calculate_signature.side_effect = ["fake_signature_old", "fake_signature_new"]
        self.fs_helper_mock.read_file.return_value = "File content"

        # Ensure the file can be 'found' and 'read' by the mocked FileSystemHelper
        self.fs_helper_mock.is_file.side_effect = lambda path: path == fake_file

        # Make sure that the read_file method will correctly return the mock content
        self.context_loader.fs_helper = self.fs_helper_mock
        
        # Method Call
        result = self.context_loader.process_file(fake_file, set())

        # Verify that load_file_content has been called
        self.assertTrue(result)
        self.assertIn(fake_file, self.context_loader.loaded_files)
        self.assertEqual(self.context_loader.loaded_files[fake_file], "### `/test_dir/file.txt`\n```plaintext\nFile content\n```")
        self.assertEqual(self.context_loader.file_signatures[fake_file], "fake_signature_new")

    def test_process_directory(self):
        fake_directory = "/test_dir"
        self.fs_helper_mock.is_dir.return_value = True
        self.context_loader.get_files_from_directory = MagicMock(return_value=["/test_dir/file1.txt"])
        self.context_loader.process_file = MagicMock(return_value=True)

        result = self.context_loader.process_directory(fake_directory, set())

        self.assertTrue(result)
        self.context_loader.get_files_from_directory.assert_called_once_with(fake_directory, set())
        self.context_loader.process_file.assert_called_once_with("/test_dir/file1.txt", set())

    def test_load_file_content(self):
        fake_file_path = "file.py"
        fake_content = "print('Hello, world!')"
        
        self.fs_helper_mock.read_file.return_value = fake_content
        self.fs_helper_mock.calculate_signature.return_value = "fake_signature"
        
        # Make sure that the read_file method will correctly return the mock content
        self.context_loader.fs_helper = self.fs_helper_mock

        self.context_loader.load_file_content(fake_file_path)

        expected_content = f"### `{fake_file_path}`\n```python\n{fake_content}\n```"
        self.assertEqual(self.context_loader.loaded_files[fake_file_path], expected_content)
        self.assertEqual(self.context_loader.file_signatures[fake_file_path], "fake_signature")

    def test_get_directories_tree(self):
        directory = "/test_dir"

        # Define different directory structures to return
        dir_structure_1 = [
            (directory, ["subdir"], ["file1.txt", "file2.py"])
        ]

        dir_structure_2 = [
            (os.path.join(directory, "subdir"), [], ["file3.js"])
        ]

        # Assign side_effect to simulate different directory states
        self.fs_helper_mock.list_dir.side_effect = [dir_structure_1, dir_structure_2]

        # Create an instance with the mocked file system helper
        context_loader = ContextLoader(api_key_loader=self.mock_api_key_loader, fs_helper=self.fs_helper_mock)

        # First call should use the first structure
        result = context_loader.get_directories_tree(directory, set())
        expected_result = "test_dir/\n    file1.txt\n    file2.py\n    subdir/\n        file3.js\n"
        self.assertEqual(result.strip(), expected_result.strip())

    def test_get_directories_tree_with_ignored_paths(self):
        directory = "/test_dir"
        
        # Define different directory structures to return
        dir_structure_1 = [
            (directory, ["subdir"], ["file1.txt", "file2.py"])
        ]

        dir_structure_2 = [
            (os.path.join(directory, "subdir"), [], ["file3.js"])
        ]

        # Assign side_effect to simulate different directory states
        self.fs_helper_mock.list_dir.side_effect = [dir_structure_1, dir_structure_2]

        # Define ignored paths
        ignore_paths = self.context_loader.normalize_paths(["/test_dir/subdir"])

        # Create an instance with the mocked file system helper
        context_loader = ContextLoader(api_key_loader=self.mock_api_key_loader, fs_helper=self.fs_helper_mock)

        # Act
        result = context_loader.get_directories_tree(directory, ignore_paths)
        
        # The ignored subdirectory should not appear in the tree
        expected_result = "test_dir/\n    file1.txt\n    file2.py\n"

        # Assert
        self.assertEqual(result.strip(), expected_result.strip())

if __name__ == '__main__':
    unittest.main()