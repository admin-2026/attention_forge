import unittest
from attention_forge.chain_steps.file_updater import FileUpdater

class TestFileUpdater(unittest.TestCase):

    def test_extract_code_blocks_single_file_with_eof(self):
        response_text = """
<`example.py`>
```
code
EOF
```
        """
        expected_output = [
            ('example.py', "code")]
        self.assertEqual(FileUpdater.extract_code_blocks(response_text), expected_output)

    def test_extract_code_blocks_single_file_with_type(self):
        response_text = """
<`example.py`>
```type
code
EOF
```
        """
        expected_output = [
            ('example.py', "code")]
        self.assertEqual(FileUpdater.extract_code_blocks(response_text), expected_output)

    def test_extract_code_blocks_multiple_files_with_eof(self):
        response_text = """
<`example1.py`>
```
code1
EOF
```
<`example2.py`>
```
code2
EOF
```
        """
        expected_output = [
            ('example1.py', "code1"),
            ('example2.py', "code2")
        ]
        self.assertEqual(FileUpdater.extract_code_blocks(response_text), expected_output)

    def test_extract_code_blocks_consecutive_code_blocks_with_eof(self):
        response_text = """
<`example.py`>
```
code part 1
EOF
```
<`example.py`>
```
code part 2
EOF
```
        """
        expected_output = [
            ('example.py', "code part 1"),
            ('example.py', "code part 2")
        ]
        self.assertEqual(FileUpdater.extract_code_blocks(response_text), expected_output)

    def test_extract_code_blocks_nested_with_eof(self):
        response_text = """
<`example.py`>
```
L2
```L3``` code ```` L3```
EOF
```
        """
        expected_output = [
            ('example.py', """L2
```L3``` code ```` L3```""")]
        self.assertEqual(FileUpdater.extract_code_blocks(response_text), expected_output)

    def test_extract_code_blocks_with_intervening_line(self):
        response_text = """
<`example.py`>
This is some line before the code block.
```type
code
EOF
```
"""
        expected_output = [
            ('example.py', "code")]
        self.assertEqual(FileUpdater.extract_code_blocks(response_text), expected_output)

    def test_extract_code_blocks_with_intervening_text(self):
        response_text = """
<`example.py`>This is some text before the code block.
```
code
EOF
```
"""
        expected_output = [
            ('example.py', "code")]
        self.assertEqual(FileUpdater.extract_code_blocks(response_text), expected_output)

    def test_extract_code_blocks_multiple_files_with_intervening_text(self):
        response_text = """
<`example1.py`>
Introduction text for the first file's code.
```
code1
EOF
```
Text between files that should be ignored.
<`example2.py`>
```
code2
EOF
```
"""
        expected_output = [
            ('example1.py', "code1"),
            ('example2.py', "code2")
        ]
        self.assertEqual(FileUpdater.extract_code_blocks(response_text), expected_output)

    def test_extract_code_blocks_with_leading_text_before_backticks(self):
        response_text = """
<`example.py`>This is some text before the code block.
some text before backticks ```
code
EOF
```
"""
        expected_output = [
            ('example.py', "code")]
        self.assertEqual(FileUpdater.extract_code_blocks(response_text), expected_output)

    def test_multiple_files_names(self):
        response_text = """
<`should_be_dropped.py`> and <`example.py`> some text
some text before backticks ```
code
EOF
```
"""
        expected_output = [
            ('example.py', "code")]
        self.assertEqual(FileUpdater.extract_code_blocks(response_text), expected_output)

if __name__ == "__main__":
    unittest.main()