import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

def extract_text(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text(separator=' ', strip=True)

def extract_links(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    links = set()
    for tag in soup.find_all('a', href=True):
        full_url = urljoin(base_url, tag['href'])
        links.add(full_url)
    return list(links)

def polite_crawl_delay(seconds=1):
    time.sleep(seconds)

def report_to_master(url, text, links):
    print(f"[Report] URL: {url}")
    print(f"[Report] Text length: {len(text)}")
    print(f"[Report] Found {len(links)} links")

def crawl_page(url):
    polite_crawl_delay(1)
    response = requests.get(url)
    html = response.text
    text = extract_text(html)
    links = extract_links(html, url)
    report_to_master(url, text, links)
    return url, text, links  # <-- Added return here!


# Example run
if __name__ == "__main__":
    crawl_page("https://en.wikipedia.org/wiki/SS_Normandie")
