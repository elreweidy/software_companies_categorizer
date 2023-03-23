from scrapping import WebScraper
from translate_json import JsonTranslator
from initial_preprocessing import JSONPreprocessor
from preprocessing import Lower
from sort_preprocessed import JsonProcessor
from classify import Categorizer
import os


def main():
    # Set up directory path
    directory_path = 'scraped_jsons'
    if not os.path.isdir(directory_path):
        os.makedirs(directory_path)

    # Scrape company data and save to JSON files
    scraper = WebScraper(csv_path='data/companies.csv', output_path=directory_path)
    scraper.scrape()

    # Preprocess JSON files (remove non-alphabetic characters and convert to lowercase)
    preprocessor = JSONPreprocessor(directory_path)
    preprocessor.preprocess()

    # Translate JSON files to English
    translator = JsonTranslator()
    translator.translate_directory(directory_path)

    # Sort preprocessed JSON files by page
    sorter = JsonProcessor(directory_path)
    sorter.preprocess_and_sort()

    # Convert text in preprocessed JSON files to lowercase
    lower = Lower(directory_path)
    lower.preprocess_lower()

    # Categorize companies based on their products and services
    categorizer = Categorizer("data/categories_updated.csv", directory_path)
    categorizer.categorize_companies()


if __name__ == "__main__":
    main()
