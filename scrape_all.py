import os
from tournament_scraper import TournamentScraper
import time

def get_tournament_urls():
    """Get all URLs from environment variables"""
    urls = []
    i = 1
    while True:
        url = os.getenv(f'TOURNAMENT_URL_{i}')
        if not url:
            break
        urls.append(url)
        i += 1
    return urls

def scrape_all():
    scraper = TournamentScraper()
    urls = get_tournament_urls()
    
    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{len(urls)}] Scraping {url}")
        try:
            scraper.scrape_tournament(url)
            time.sleep(2)  # Be polite
        except Exception as e:
            print(f"! Failed: {str(e)}")

if __name__ == "__main__":
    scrape_all()