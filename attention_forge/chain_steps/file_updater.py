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
        - Looks for file names in `<FILE_NAME>`.
        - Skips text until encountering a ``` line, then begins recording.
        - Ignores any optional text after ``` and before the code.
        - Logs file content until "EOF" followed by ``` is found.
        """
        extracted_files = []
        current_file = None
        code_content = []
        in_code_block = False
        found_eof = False

        lines = response_text.split('\n')

        for idx, line in enumerate(lines):
            stripped_line = line.strip()

            # Detect filename header
            new_file_name = FileUpdater.extract_filenames(stripped_line)
            if len(new_file_name) > 0:
                # If EOF was not found for the previous file, print a warning
                if current_file and not found_eof:
                    print(f"⚠️ Warning: 'EOF' not found for the file: {current_file}")

                if current_file:
                    extracted_files.append((current_file, '\n'.join(code_content).strip()))
                    in_code_block = False  # Reset in_code_block after EOF
                    current_file = None  # Clear file name to look for a new one
                    found_eof = False

                # Start processing a new file
                current_file = new_file_name[0]
                code_content = []  # Reset code content for the new file
                in_code_block = False  # Reset in_code_block status
                found_eof = False
                continue

            # Start of a new code block
            if not in_code_block and stripped_line.startswith('```'):
                in_code_block = True
                continue

            # Handling for "EOF" followed by ending code block
            if in_code_block and stripped_line == 'EOF':
                eof_line_index = idx + 1
                if eof_line_index < len(lines) and lines[eof_line_index].strip() == '```':
                    # Finish current code block
                    extracted_files.append((current_file, '\n'.join(code_content).strip()))
                    in_code_block = False  # Reset in_code_block after EOF
                    current_file = None  # Clear file name to look for a new one
                    found_eof = True
                    continue
                else:
                    found_eof = False
                    print(f"⚠️ Warning: 'EOF' found, but no code block end backticks: {current_file}")

            # Collect code content if within the code block
            if in_code_block and current_file:
                code_content.append(line)

        # If EOF was never found for the last file, print a warning
        if current_file and not found_eof and code_content:
            extracted_files.append((current_file, '\n'.join(code_content).strip()))
            print(f"⚠️ Warning: 'EOF' not found for the file: {current_file}")

        return extracted_files
    
    @staticmethod
    def extract_filenames(text):
        # Regex pattern to match filenames inside angle brackets
        pattern = r'<`([^`]+)`>'
        filenames = re.findall(pattern, text)
        return filenames