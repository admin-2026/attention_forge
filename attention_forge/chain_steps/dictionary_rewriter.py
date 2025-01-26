from attention_forge.chain_steps.step import Step

class DictionaryRewriter(Step):
    def __init__(self, query):
        self.query = query

    def run(self, input_data=None):
        result = self.apply_query(input_data)
        return result

    def apply_query(self, input_data):
        result = {} if isinstance(input_data, dict) else []

        # Process each rule in the query
        for rule in self.query:
            from_path = rule.get('from', '')
            to_path = rule.get('to', '')

            source_value = self.get_value_by_path(input_data, from_path.split('.'))

            if to_path == ".":
                result = source_value
            else:
                self.set_value_by_path(result, to_path.split('.'), source_value)

        return result

    def get_value_by_path(self, data, path):
        if not path or path == [""]:
            return data

        current_data = data
        for key in path:
            if isinstance(current_data, dict) and key in current_data:
                current_data = current_data[key]
            else:
                raise KeyError(f"Key '{key}' not found in the data at path '{'.'.join(path)}'")
        return current_data

    def set_value_by_path(self, data, path, value):
        if not path:
            return
        
        if isinstance(data, dict):
            current_data = data
            last_key = path[-1]
            for key in path[:-1]:
                if key not in current_data:
                    current_data[key] = {}
                current_data = current_data[key]
            current_data[last_key] = value
        else:
            raise TypeError("Output data structure must be a dictionary to set values by path.")