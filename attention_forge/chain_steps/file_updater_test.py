import unittest
from attention_forge.chain_steps.file_updater import FileUpdater

class TestFileUpdater(unittest.TestCase):

    def test_extract_code_blocks_single_file(self):
        response_text = """
<`example.py`>
```
code
```
        """
        expected_output = [
            ('example.py', "code")]
        self.assertEqual(FileUpdater.extract_code_blocks(response_text), expected_output)

    def test_extract_code_blocks_multiple_files(self):
        response_text = """
<`example1.py`>
```
code1
```
<`example2.py`>
```
code2
```
        """
        expected_output = [
            ('example1.py', "code1"),
            ('example2.py', "code2")
        ]
        self.assertEqual(FileUpdater.extract_code_blocks(response_text), expected_output)

    def test_extract_code_blocks_no_file(self):
        response_text = "This is a plain text response without code blocks."
        expected_output = []
        self.assertEqual(FileUpdater.extract_code_blocks(response_text), expected_output)

    def test_extract_code_blocks_nested_backticks(self):
        response_text = """
<`example.py`>
```
```example```
```
        """
        expected_output = [
            ('example.py', "```example```")]
        self.assertEqual(FileUpdater.extract_code_blocks(response_text), expected_output)

    def test_extract_code_blocks_no_file_header(self):
        response_text = """
```
code
```
        """
        expected_output = []
        self.assertEqual(FileUpdater.extract_code_blocks(response_text), expected_output)

    def test_extract_code_blocks_consecutive_code_blocks(self):
        response_text = """
<`example.py`>
```
code part 1
```
```
code part 2
```
        """
        expected_output = [
            ('example.py', """code part 1
code part 2""")]
        self.assertEqual(FileUpdater.extract_code_blocks(response_text), expected_output)

    def test_extract_code_blocks_with_language(self):
        response_text = """
<`example.py`>
```python
def hello():
    print("Hello, World!")
```
        """
        expected_output = [
            ('example.py', """def hello():
    print("Hello, World!")""")]
        self.assertEqual(FileUpdater.extract_code_blocks(response_text), expected_output)

    def test_extract_code_blocks_three_levels_nested(self):
        response_text = """
<`example.py`>
```
L2
```L3``` code ```` L3```
L2
```
        """
        expected_output = [
            ('example.py', """L2
```L3``` code ```` L3```
L2""")]
        self.assertEqual(FileUpdater.extract_code_blocks(response_text), expected_output)

    # def test_extract_code_blocks_multiple_code_blocks_inside_code_block(self):
        # response_text = """
# <`example.py`>
# ```
# start
    # ```
    # code 1
    # ```
    # code 2
    # ```
    # code 3
    # ```
# end
# ```
        # """
        # expected_output = [
            # ('example.py', """start
    # ```
    # code 1
    # ```
    # code 2
    # ```
    # code 3
    # ```
# end""")]
        # self.assertEqual(FileUpdater.extract_code_blocks(response_text), expected_output)

    # def test_extract_code_blocks_four_levels_of_nesting(self):
        # response_text = """
# <`example.py`>
# ```
# L2 start
# ```
# L3 start
# ```
# L4 start
# ```
# code
# ```
# L4 end
# ```
# L3 end
# ```
# L2 end
# ```
        # """
        # expected_output = [
            # ('example.py', """L2 start
# ```
# L3 start
# ```
# L4 start
# ```
# code
# ```
# L4 end
# ```
# L3 end
# ```
# L2 end""")]
        # self.assertEqual(FileUpdater.extract_code_blocks(response_text), expected_output)

    def test_extract_code_blocks_multiple_blocks_inside_nested(self):
        response_text = """
<`example.py`>
```
L2
    ```code 1```
    ```code 2```
L2
```
        """
        expected_output = [
            ('example.py', """L2
    ```code 1```
    ```code 2```
L2""")]
        self.assertEqual(FileUpdater.extract_code_blocks(response_text), expected_output)

if __name__ == "__main__":
    unittest.main()
