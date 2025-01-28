import re
from attention_forge.chain_steps.step import Step
from attention_forge.file_manager import update_file

class FileUpdater(Step):
    def run(self, *response_texts):
        """Parses response text and updates extracted files."""
        combined_text = ' '.join(response_texts)
        extracted_files = self.extract_code_blocks(combined_text)

        if not extracted_files:
            print("⚠️ No file updates detected in the response.")
            return

        for file_name, code_content in extracted_files:
            print(f"🔍 Processing file update: {file_name}")
            update_file(file_name, code_content)
        return None

    @staticmethod
    def extract_code_blocks(response_text):
        """
        Extracts file names and code blocks from responses.
        - Handles code blocks with optional language specifiers.
        - Merges consecutive code blocks under the same file.
        - Ignores lines with triple backticks unless they are exact end delimiters.
        """
        extracted_files = []
        current_file = None
        code_content = []
        in_code_block = False  # Tracks if we're inside a code block

        lines = response_text.split('\n')

        for line in lines:
            stripped_line = line.strip()

            # Detect filename header
            if stripped_line.startswith('<`') and stripped_line.endswith('`>'):
                if current_file is not None and code_content:
                    extracted_files.append((current_file, '\n'.join(code_content).strip()))
                    code_content = []
                current_file = stripped_line[2:-2]
                in_code_block = False  # Reset code block state for new file
                continue

            # Check for code block start (any line starting with ```)
            if not in_code_block and stripped_line.startswith('```'):
                in_code_block = True
                continue  # Skip the start line

            # Check for code block end (exactly ```)
            if in_code_block and stripped_line == '```':
                in_code_block = False
                continue  # Skip the end line

            # Collect code content if within a code block and a file is active
            if in_code_block and current_file is not None:
                code_content.append(line)

        # Add remaining code content if any
        if current_file is not None and code_content:
            extracted_files.append((current_file, '\n'.join(code_content).strip()))

        return extracted_files