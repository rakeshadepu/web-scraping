from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
import re
import pprint

class NailibScraper:
    BASE_URL = "https://nailib.com"
    
    # MongoDB connection setup
    def __init__(self):
        self.client = MongoClient("should be replaced with your mongodb url")
        # replace <password> with your monogodab password
        self.db = self.client['nailib_database']  # Database name
        self.collection = self.db['sample_data']  # Collection name

    def fetch_page(self, url):
        # try catch block for fetching url 
        try:
            response = requests.get(url) #gets url
            response.raise_for_status() # checks status of url
            return response.text 
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page: {e}")
            return None

    def parse_sample(self, html):
        # parsing data using beautifulsoap
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('h1').string.strip() if soup.find('h1') else None
        subject_element = soup.find('h2', class_='file_sample__body__container__middle__cover__heading--small__gzm_v')
        subject = subject_element.get_text(strip=True) if subject_element else None
        description = soup.find('meta', {'name': 'description'})['content'] if soup.find('meta', {'name': 'description'}) else None
        word_count = self.extract_word_count(soup) # word count div
        file_link = self.extract_file_link(soup) #file link
        time_estimate = self.extract_time_estimate(soup)

        # Extract sections from the table of contents
        sections = self.extract_sections_from_toc(soup)

        return {
            "title": title,
            "subject": subject,
            "description": description,
            "sections": sections,
            "word_count": word_count,
            "time_estimate": time_estimate,
            "file_link": file_link,
            "publication_date": None
        }
    
    def store_data_to_mongodb(self, data):
        try:
            # Use upsert to avoid duplicates
            self.collection.update_one(
                {"title": data['title']},  # You can use other unique identifiers here if necessary
                {"$set": data},
                upsert=True
            )
            print("Data stored successfully.")
        except Exception as e:
            print(f"Error storing data: {e}")
        
    def display_data_from_mongodb(self):
        try:
            # Fetch data from MongoDB
            documents = self.collection.find()
            print("\nStored Data:")
            for document in documents:
                pprint.pprint(document)  # Pretty print for readability
        except Exception as e:
            print(f"Error fetching data: {e}")

    def extract_word_count(self, soup):
        # extraction of word count function
        word_count_div = soup.find('div', class_='file_sample__body__container__middle__cover__list__nmVAV')
        if word_count_div:
            for child in word_count_div.find_all('div'):
                if 'Word count:' in child.get_text(strip=True):
                    word_count_match = re.search(r'Word count:\s*([\d,]+)', child.get_text(strip=True))
                    if word_count_match:
                        return word_count_match.group(1).replace(',', '')
        return None

    def extract_file_link(self, soup):
        link = soup.find('a', href=re.compile(r'.*\.pdf$'))
        return f"{self.BASE_URL}{link['href']}" if link else None

    def extract_time_estimate(self, soup):
        # time taken data function
        time_estimate_div = soup.find('div', class_='file_sample__body__container__middle__cover__stat__RuwZ1')
        if time_estimate_div:
            time_text = time_estimate_div.find_all('div', class_='file_sample__body__container__middle__cover__stat__item__text__6umeQ')
            if time_text:
                time_estimate = time_text[-1].get_text(strip=True)
                return time_estimate.replace(' read', '')
        return None

    def extract_sections_from_toc(self, soup):
        # sections data extraction function
        sections = []
        toc_items = soup.find_all('ul', class_='file_toc__KmF9d')
        
        for toc_item in toc_items:
            link = toc_item.find('a', class_='file_toc__link__eLvZJ')
            if link:
                section_title = link.get_text(strip=True)
                if section_title not in sections:
                    sections.append(section_title)
        
        return sections

    def scrape_sample_page(self, url):
        html = self.fetch_page(url)
        if html:
            return self.parse_sample(html)
        return None

    def upsert_to_mongodb(self, data):
        # Use upsert to prevent duplication
        filter = {"title": data["title"], "subject": data["subject"]}
        update = {"$set": data}
        result = self.collection.update_one(filter, update, upsert=True)
        if result.upserted_id:
            print(f"Data inserted with ID: {result.upserted_id}")
        else:
            print("Data updated.")

# Create an instance of the scraper
scraper = NailibScraper()

# Test URL and this should be changed to check for multiple pages of this websites
url = "https://nailib.com/ia-sample/ib-math-ai-sl/64ae3a2051c461c33d2e28d9"

# Scrape the sample page
result = scraper.scrape_sample_page(url)

# If data was scraped successfully, send it to MongoDB
if result:
    scraper.upsert_to_mongodb(result)
else:
    print("Scraping failed or no data found.")

# Optionally, display data from MongoDB to check what's stored
scraper.display_data_from_mongodb()
