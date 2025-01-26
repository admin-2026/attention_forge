import re
from attention_forge.chain_steps.step import Step
from attention_forge.file_manager import update_file

class FileUpdater(Step):
    def run(self, response_text):
        """Parses response text and updates extracted files."""
        extracted_files = self.extract_code_blocks(response_text)

        if not extracted_files:
            print("⚠️ No file updates detected in the response.")
            return

        for file_name, code_content in extracted_files:
            print(f"🔍 Processing file update: {file_name}")
            update_file(file_name, code_content)
        return None

    def extract_code_blocks(self, response_text):
        """
        Extracts file names and code blocks from responses.

        Expected Response Format:
        ```
        ### `filename.ext`
        ```language
        <code>
        ```
        ```
        """
        # Updated regex pattern: Extracts filenames inside backticks (`file.ext`)
        pattern = r"<`(.+?)`>\s*\n```(\w+)?\n(.*?)\n```"

        matches = re.findall(pattern, response_text, re.DOTALL)

        extracted_files = []
        for match in matches:
            file_name, _, code_content = match
            extracted_files.append((file_name.strip(), code_content.strip()))

        return extracted_files