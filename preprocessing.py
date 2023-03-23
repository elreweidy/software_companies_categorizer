import os
import json
import re


class Lower:

    def __init__(self, json_dir):
        self.json_dir = json_dir
        self.regex = re.compile('[^a-zA-Z ]')

    def preprocess_lower(self):
        for filename in os.listdir(self.json_dir):
            if filename.endswith('.json'):
                with open(os.path.join(self.json_dir, filename), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                for key in data.keys():
                    if isinstance(data[key], str):
                        # remove non-alphabetic characters and convert to lowercase
                        data[key] = self.regex.sub('', data[key].lower())
                    elif isinstance(data[key], list):
                        for i, lst in enumerate(data[key]):
                            for j, string in enumerate(lst):
                                if isinstance(string, str):
                                    # remove non-alphabetic characters and convert to lowercase
                                    data[key][i][j] = self.regex.sub('', string.lower())
                with open(os.path.join(self.json_dir, filename), 'w', encoding='utf-8') as f:
                    json.dump(data, f)
