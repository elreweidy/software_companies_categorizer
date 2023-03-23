import requests
from bs4 import BeautifulSoup
import json
import csv
import time


class WebsiteCrawler:
    def __init__(self, companies_csv):
        self.companies_csv = companies_csv
        self.companies = self._load_companies()
        self.crawled_pages = set()  # Keep track of crawled pages

    def _load_companies(self):
        with open(self.companies_csv, newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            companies = []
            for row in reader:
                companies.append(row)
            return companies

    def _get_page(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            return None

    def _parse_page(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'span', 'a']
        data = {}
        for tag in tags:
            data[tag] = []
            for element in soup.find_all(tag):
                text = element.get_text().strip()
                if text:
                    data[tag].append(text)
        return data

    def _crawl_links(self, url, start_time):
        if url in self.crawled_pages:
            return {}

        elapsed_time = time.monotonic() - start_time
        if elapsed_time > 20:  # Check if the timeout is reached
            print(f"Timeout reached for {url}")
            return {}

        page = self._get_page(url)
        if page:
            self.crawled_pages.add(url)
            data = self._parse_page(page)
            soup = BeautifulSoup(page, 'html.parser')
            links = [link.get('href') for link in soup.find_all('a')]
            for link in links:
                if link is None:  # Skip None links
                    continue
                if link.startswith('https'):
                    try:
                        self._crawl_links(link, start_time)
                    except Exception as e:
                        print(f"Error crawling {link}: {e}")
                elif link.startswith('/'):
                    try:
                        self._crawl_links(url + link, start_time)
                    except Exception as e:
                        print(f"Error crawling {url+link}: {e}")
            return data
        else:
            return {}

    def crawl_websites(self):
        results = {}
        for company in self.companies:
            url = company['Corporate website']
            print(f"Crawling {url}")
            try:
                start_time = time.monotonic()
                data = self._crawl_links(url, start_time)
                if data:
                    results[company['Company name']] = data
            except Exception as e:
                print(f"Error crawling {url}: {e}")
        with open('results.json', 'w') as outfile:
            json.dump(results, outfile, indent=4)

crawler = WebsiteCrawler('data/companies.csv')
crawler.crawl_websites()
