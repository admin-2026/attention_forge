import re
from file_manager import update_file

def extract_code_blocks(response_text):
    """Extracts file names and code blocks from OpenAI responses."""
    pattern = r"### (.+?):\n```(\w+)?\n(.*?)\n```"
    matches = re.findall(pattern, response_text, re.DOTALL)

    extracted_files = []
    for match in matches:
        file_name, _, code_content = match
        extracted_files.append((file_name.strip(), code_content.strip()))

    return extracted_files

def process_openai_response(response_text):
    """Parses OpenAI response and updates extracted files."""
    extracted_files = extract_code_blocks(response_text)

    if not extracted_files:
        print("⚠️ No file updates detected in the OpenAI response.")
        return

    for file_name, code_content in extracted_files:
        print(f"🔍 Processing file update: {file_name}")
        update_file(file_name, code_content)
