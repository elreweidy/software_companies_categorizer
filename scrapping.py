import requests
from bs4 import BeautifulSoup
import csv
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

class WebScraper:
    def __init__(self, csv_path, output_path):
        self.csv_path = csv_path
        self.output_path = output_path
        self.output = {}
        self.options = Options()
        self.options.headless = True
        self.driver = webdriver.Chrome(options=self.options)

    def scrape(self):
        with open(self.csv_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                url = "https://"+row['Corporate website']
                company_name = row['Company name']
                if url.startswith('http'):
                    self._scrape_url(url, company_name)

        self.driver.quit()

    def _scrape_url(self, url, company_name):
        try:
            self.driver.get(url)
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            # Scrape the website content and linked pages
            data = {}
            for tag in soup.find_all():
                if tag.text.strip() != '':
                    if tag.name not in data:
                        data[tag.name] = {
                            'this_page': [],
                            'linked_pages': []
                        }
                    text = tag.text.strip().replace('\n', '').replace('\r', '').replace('\t', '')
                    data[tag.name]['this_page'].append(text)

            links = soup.find_all('a')
            for link in links:
                link_url = link.get('href')
                if link_url and 'http' in link_url:
                    try:
                        self.driver.get(link_url)
                        linked_html = self.driver.page_source
                        linked_soup = BeautifulSoup(linked_html, 'html.parser')
                        for tag in linked_soup.find_all():
                            if tag.text.strip() != '':
                                if tag.name in data:
                                    text = tag.text.strip().replace('\n', '').replace('\r', '').replace('\t', '')
                                    data[tag.name]['linked_pages'].append(text)
                    except WebDriverException as e:
                        print(f"Could not scrape {link_url}: {e}")
                        continue

        except WebDriverException as e:
            print(f"Could not scrape {url}: {e}")
            return

        # Sort the scraped data
        tag_order = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'a', 'span', 'li', 'div']
        sorted_data = {tag: data[tag] for tag in tag_order if tag in data}

        # Create output for the company
        output = {}
        for tag in sorted_data:
            output[tag] = [
                sorted_data[tag]['this_page'],
                sorted_data[tag]['linked_pages']
            ]

        # Write output to a JSON file for the company
        with open(f'{self.output_path}/{company_name}.json', 'w', encoding='utf-8') as jsonfile:
            json.dump(output, jsonfile, ensure_ascii=False, indent=4)
        print(f"Scraped data for '{company_name}' has been written to {self.output_path}/{company_name}.json")
        
        self.output[company_name] = output

    def write_all_output(self):
        for company, output in self.output.items():
            with open(f'{self.output_path}/{company}.json', 'w', encoding='utf-8') as jsonfile:
                json.dump(output, jsonfile, ensure_ascii=True, indent=4)
            print(f"Scraped data for '{company}' has been written to {company}.json")