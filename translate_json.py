import os
import json
import math
from googletrans import LANGUAGES, Translator
from multiprocessing import Pool, cpu_count
import time

class JsonTranslator:
    def __init__(self, src_lang="auto", dest_lang="en"):
        self.translator = Translator()
        self.src_lang = src_lang
        self.dest_lang = dest_lang

    def translate_directory(self, directory):
        for filename in os.listdir(directory):
            if filename.endswith('.json'):
                filepath = os.path.join(directory, filename)
                with open(filepath, "r") as f:
                    data = json.load(f)
                self._translate_dict(data)
                with open(filepath, "w") as f:
                    json.dump(data, f, indent=2)

    def _translate_dict(self, d):
        for k, v in d.items():
            if isinstance(v, dict):
                self._translate_dict(v)
            elif isinstance(v, list):
                for i, lst in enumerate(v):
                    if isinstance(lst, list):
                        for j, txt in enumerate(lst):
                            if isinstance(txt, str) and txt.strip():
                                # split text into chunks of 500 characters or less
                                chunks = [txt[k:k+400] for k in range(0, len(txt), 400)]
                                # translate each chunk and join them back
                                translated_chunks = []
                                for chunk in chunks:
                                    try:
                                        translation = self.translator.translate(chunk, src=self.src_lang, dest=self.dest_lang).text
                                        # time.sleep(1)
                                        # Write the translated chunk in the json file
                                        translated_chunks.append(translation)
                                    except AttributeError as e:
                                        print(f"Error translating {k}[{i}][{j}]: {e}")
                                        continue
                                v[i][j] = ' '.join(translated_chunks) if translated_chunks else txt
                            elif isinstance(txt, str) and not txt.strip():
                                # Skip empty strings
                                continue
                            else:
                                try:
                                    # Translate single word or short phrases
                                    translation = self.translator.translate(txt, src=self.src_lang, dest=self.dest_lang).text
                                    v[i][j] = translation
                                except Exception as e:
                                    print(f"Error translating {k}[{i}][{j}]: {e}")
                                    continue
