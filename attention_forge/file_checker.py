import os
import subprocess

class FileChecker():
    def __init__(self, context_file='attention_forge_context.yaml', project_file='attention_forge_project.yaml'):
        self.context_file = context_file
        self.project_file = project_file

    def run(self, *input_data):
        context_exists = os.path.isfile(self.context_file)
        project_exists = os.path.isfile(self.project_file)

        if not context_exists or not project_exists:
            response = input(f"Files '{self.context_file}' and/or '{self.project_file}' not found. Do you want attention-forge to create these files for you? (yes/no): ").strip().lower()
            if response == 'yes':
                try:
                    subprocess.run(['attention-forge-init'], check=True)
                    return {'status': 'initialized'}
                except subprocess.CalledProcessError as e:
                    print("An error occurred while initializing the files:", e)
                    return {'status': 'error'}
            else:
                print(f"'{self.context_file}' and '{self.project_file}' are required to run attention-forge.")
                return {'status': 'not_initialized'}
        else:
            return {'status': 'exists'}