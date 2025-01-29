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
        - Recognizes "EOF" as the end of file content marker.
        Warns if file content is found without "EOF".
        """
        extracted_files = []
        current_file = None
        code_content = []
        in_code_block = False
        eof_detected = False

        lines = response_text.split('\n')

        for line in lines:
            stripped_line = line.strip()

            # Detect filename header
            if stripped_line.startswith('<`') and stripped_line.endswith('`>'):
                if current_file is not None and code_content:
                    if not eof_detected:
                        print(f"⚠️ Warning: EOF not detected for file '{current_file}'.")
                    extracted_files.append((current_file, '\n'.join(code_content).strip()))
                    code_content = []
                current_file = stripped_line[2:-2]
                in_code_block = False
                eof_detected = False
                continue

            # Check for start of code block
            if not in_code_block and stripped_line.startswith('```'):
                in_code_block = True
                continue

            # Detect "EOF" which signals the end of content
            if in_code_block and stripped_line == 'EOF':
                in_code_block = False
                eof_detected = True
                # Move forward to capture any immediately following end block
                continue

            # Check for code block end
            if not in_code_block and stripped_line == '```':
                continue

            # Collect code content if within code block
            if in_code_block and current_file is not None:
                code_content.append(line)

        # Add remaining code content if any
        if current_file is not None and code_content:
            if not eof_detected:
                print(f"⚠️ Warning: EOF not detected for file '{current_file}'.")
            extracted_files.append((current_file, '\n'.join(code_content).strip()))

        return extracted_files