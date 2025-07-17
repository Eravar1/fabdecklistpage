from bs4 import BeautifulSoup
from aiohttp import ClientSession
import logging

logger = logging.getLogger(__name__)

class FABScraper:
    """Handles all web scraping operations for Flesh and Blood data"""
    
    def __init__(self):
        self.http_session = None
    
    async def __aenter__(self):
        self.http_session = ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.http_session:
            await self.http_session.close()
    
    async def get_pairings(self, url):
        """Get pairings from coverage page"""
        try:
            async with self.http_session.get(url) as response:
                if response.status == 200:
                    soup = BeautifulSoup(await response.text(), 'html.parser')
                    pairings = {}
                    
                    for row in soup.find_all('div', class_='tournament-coverage__row--results'):
                        players = row.find_all('div', class_='tournament-coverage__player')
                        if len(players) >= 2:
                            p1 = players[0].find('span').get_text(strip=True)
                            p2 = players[1].find('span').get_text(strip=True)
                            pairings[p1] = p2
                            pairings[p2] = p1
                    return pairings
                logger.warning(f"Failed to fetch pairings: HTTP {response.status}")
                return None
        except Exception as e:
            logger.error(f"Error getting pairings: {e}")
            return None

    async def get_decklist_data(self, url):
        """Scrape decklist data from URL"""
        try:
            async with self.http_session.get(url) as response:
                if response.status == 200:
                    soup = BeautifulSoup(await response.text(), 'html.parser')
                    
                    decklist = {
                        'hero': None,
                        'equipment': [],
                        'cards': []
                    }
                    
                    # Extract hero
                    hero_div = soup.find('div', class_='decklist-hero')
                    if hero_div:
                        decklist['hero'] = hero_div.get_text(strip=True)
                    
                    # Extract equipment
                    for equip in soup.find_all('div', class_='decklist-equipment'):
                        decklist['equipment'].append(equip.get_text(strip=True))
                    
                    # Extract cards
                    for card_row in soup.find_all('tr', class_='decklist-card'):
                        cols = card_row.find_all('td')
                        if len(cols) >= 2:
                            quantity = cols[0].get_text(strip=True)
                            name = cols[1].get_text(strip=True)
                            decklist['cards'].append(f"{quantity}x {name}")
                    
                    return decklist
                logger.warning(f"Failed to fetch decklist: HTTP {response.status}")
                return None
        except Exception as e:
            logger.error(f"Error scraping decklist: {e}")
            return None