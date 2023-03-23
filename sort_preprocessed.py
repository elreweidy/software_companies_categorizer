import os
import json

class JsonProcessor:
    
    def __init__(self, dir_path):
        self.dir_path = dir_path
        
    def preprocess_and_sort(self):
        for file_name in os.listdir(self.dir_path):
            if file_name.endswith('.json'):
                file_path = os.path.join(self.dir_path, file_name)
                with open(file_path, 'r') as f:
                    data = json.load(f)
                preprocessed_data = self.preprocess(data)
                with open(file_path, 'w') as f:
                    json.dump(preprocessed_data, f, indent=4)
    
    def preprocess(self, data):
        first_page = []
        other_pages = []
        for key, value in data.items():
            if isinstance(value, list):
                if len(first_page) == 0:
                    first_page = value
                else:
                    other_pages.append(value)
        return {"first_page": [first_page], "other_pages": [other_pages]}

