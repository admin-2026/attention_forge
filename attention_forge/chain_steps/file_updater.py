import re
from attention_forge.chain_steps.step import Step
from attention_forge.file_manager import update_file

class FileUpdater(Step):
    def run(self, response_text):
        """Parses response text and updates extracted files."""
        # Extract code blocks and corresponding file names from the response
        extracted_files = self.extract_code_blocks(response_text)

        # If no file updates are detected, print a warning message
        if not extracted_files:
            print("⚠️ No file updates detected in the response.")
            return

        # Iterate over each extracted file and update it with the new content
        for file_name, code_content in extracted_files:
            print(f"🔍 Processing file update: {file_name}")
            update_file(file_name, code_content)
        return None

    def extract_code_blocks(self, response_text):
        """
        Extracts file names and code blocks from responses using line-by-line parsing.
        Handles code content with nested triple backticks correctly.
        """
        extracted_files = []  # List to store tuples of (file name, code content)
        current_file = None   # Currently identified file name
        code_content = []     # Accumulated code content for the current file
        inside_code_block = False  # Flag to track if we are inside a code block

        # Split response text into separate lines
        lines = response_text.split('\n')

        # Process each line to find file headers and code blocks
        for i, line in enumerate(lines):
            stripped_line = line.strip()

            # Detect filename header, indicated by <`filename`>
            if stripped_line.startswith('<`') and stripped_line.endswith('`>'):
                # If there is an existing file being processed, save its content
                if current_file is not None and code_content:
                    extracted_files.append((current_file, '\n'.join(code_content).strip()))
                    code_content = []  # Reset code content for new file
                current_file = stripped_line[2:-2]  # Get filename by stripping markers
                continue

            # Detect start or end of a code block marked by ```
            if stripped_line.startswith('```') and (not inside_code_block or len(stripped_line) == 3):
                if inside_code_block:
                    # Ending a code block
                    inside_code_block = False
                    continue
                else:
                    # Starting a code block
                    inside_code_block = True
                    continue

            # Collect code content lines if within a code block and a file context
            if current_file is not None and inside_code_block:
                code_content.append(line)

        # Handle case where the response ends while still in a code block
        if current_file is not None and code_content:
            extracted_files.append((current_file, '\n'.join(code_content).strip()))

        return extracted_files