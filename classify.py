import csv
import json
import os


class Categorizer:
    def __init__(self, categories_file, data_dir):
        self.categories = {}
        with open(categories_file, newline='') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)  # skip the header row
            for row in reader:
                category, keywords = row[1], row[2:]
                self.categories[category] = keywords
        self.data_dir = data_dir
    
    def count_category_scores(self, data):
        category_scores = []  # create a list to store scores for each category
        for category in self.categories:
            category_keywords = self.categories[category]
            score = 0
            for key in data:
                for page in data[key]:
                    for i, lst in enumerate(page):
                        for j, text in enumerate(lst):
                            for keyword in category_keywords:
                                if keyword in text:
                                    score += (len(lst) - j) * (len(page) - i)
            category_scores.append(score)  # append score for current category to list
        return category_scores  # return list of scores for each category

    
    def categorize_companies(self):
        results = []
        for filename in os.listdir(self.data_dir):
            company_name = os.path.splitext(filename)[0]
            with open(os.path.join(self.data_dir, filename)) as f:
                data = json.load(f)
            
            company_scores = {}
            scores = self.count_category_scores(data)
            if all(score == 0 for score in scores):
                company_category = "Other"
            else:
                max_score = max(scores)
                company_category = [category for category, score in zip(self.categories, scores) if score == max_score][0]

            company_result = {
                'company_name': company_name,
                'scores': scores,
                'main_category': company_category
            }
            
            results.append(company_result)
        
        with open('results.json', 'w') as f:
            json.dump(results, f)
