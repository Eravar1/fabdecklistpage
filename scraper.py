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

    # async def get_decklist_data(self, url):
    #     """Scrape decklist data from URL"""
    #     try:
    #         async with self.http_session.get(url) as response:
    #             if response.status == 200:
    #                 soup = BeautifulSoup(await response.text(), 'html.parser')
                    
    #                 decklist = {
    #                     'hero': None,
    #                     'equipment': [],
    #                     'cards': []
    #                 }
                    
    #                 # Extract hero
    #                 hero_div = soup.find('div', class_='decklist-hero')
    #                 if hero_div:
    #                     decklist['hero'] = hero_div.get_text(strip=True)
                    
    #                 # Extract equipment
    #                 for equip in soup.find_all('div', class_='decklist-equipment'):
    #                     decklist['equipment'].append(equip.get_text(strip=True))
                    
    #                 # Extract cards
    #                 for card_row in soup.find_all('tr', class_='decklist-card'):
    #                     cols = card_row.find_all('td')
    #                     if len(cols) >= 2:
    #                         quantity = cols[0].get_text(strip=True)
    #                         name = cols[1].get_text(strip=True)
    #                         decklist['cards'].append(f"{quantity}x {name}")
                    
    #                 return decklist
    #             logger.warning(f"Failed to fetch decklist: HTTP {response.status}")
    #             return None
    #     except Exception as e:
    #         logger.error(f"Error scraping decklist: {e}")
    #         return None
        
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
                    
                    # Extract hero from player info section
                    player_info = soup.find('div', class_='player-info')
                    if player_info:
                        player_name_h2 = player_info.find('h2')
                        if player_name_h2:
                            hero_text = player_name_h2.get_text(strip=True)
                            # Extract hero name from format: "Player Name (ID) - Hero Name - Format"
                            parts = hero_text.split(' - ')
                            if len(parts) >= 2:
                                decklist['hero'] = parts[1]
                    
                    # Try to find list view first (more structured)
                    list_view = soup.find('section', class_='decklist-list-view')
                    if list_view and 'hidden' not in list_view.get('class', []):
                        # Extract from list view
                        self._extract_from_list_view(list_view, decklist)
                    else:
                        # Fallback to grid view
                        grid_view = soup.find('section', class_='decklist-grid-view')
                        if grid_view:
                            self._extract_from_grid_view(grid_view, decklist)
                    
                    return decklist
                logger.warning(f"Failed to fetch decklist: HTTP {response.status}")
                return None
        except Exception as e:
            logger.error(f"Error scraping decklist: {e}")
            return None

    def _extract_from_list_view(self, list_view, decklist):
        """Extract decklist data from list view"""
        # Extract Hero/Weapon/Equipment section
        hero_section = list_view.find('div', class_='list-view-container', string=lambda text: text and 'Hero / Weapon / Equipment' in text)
        if not hero_section:
            hero_section = list_view.find('h3', string=lambda text: text and 'Hero / Weapon / Equipment' in text)
            if hero_section:
                hero_section = hero_section.find_parent('div', class_='list-view-container')
        
        if hero_section:
            cards_container = hero_section.find('ul', class_='cards-container')
            if cards_container:
                for card_item in cards_container.find_all('li', class_='card-item'):
                    card_name_div = card_item.find('div', class_='card-name')
                    if card_name_div:
                        card_text = card_name_div.get_text(strip=True)
                        # Extract quantity and name
                        if 'x' in card_text:
                            quantity, name = card_text.split('x', 1)
                            quantity = quantity.strip()
                            name = name.strip()
                            decklist['equipment'].append(f"{quantity}x {name}")
                            
                            # Check if this is the hero card
                            if decklist['hero'] and decklist['hero'].lower() in name.lower():
                                decklist['hero'] = name  # Use the exact name from the decklist
        
        # Extract cards from pitch sections
        pitch_section = list_view.find('section', class_='pitch-section')
        if pitch_section:
            for pitch_container in pitch_section.find_all('div', class_='list-view-container'):
                cards_container = pitch_container.find('ul', class_='cards-container')
                if cards_container:
                    for card_item in cards_container.find_all('li', class_='card-item'):
                        card_name_div = card_item.find('div', class_='card-name')
                        if card_name_div:
                            card_text = card_name_div.get_text(strip=True)
                            decklist['cards'].append(card_text)

    def _extract_from_grid_view(self, grid_view, decklist):
        """Extract decklist data from grid view"""
        # Extract Hero/Weapon/Equipment section
        hero_heading = grid_view.find('h3', string=lambda text: text and 'Hero / Weapon / Equipment' in text)
        if hero_heading:
            # Find the cards container after the hero heading
            next_elem = hero_heading.find_next_sibling('div', class_='cards-container')
            if next_elem:
                for card_div in next_elem.find_all('div'):  # Each card is in a div
                    card_name_div = card_div.find('div', class_='card-name')
                    if card_name_div:
                        card_text = card_name_div.get_text(strip=True)
                        decklist['equipment'].append(card_text)
                        
                        # Check if this is the hero card
                        if decklist['hero'] and decklist['hero'].lower() in card_text.lower():
                            # Extract just the name without quantity
                            if 'x' in card_text:
                                _, name = card_text.split('x', 1)
                                decklist['hero'] = name.strip()
        
        # Extract cards from pitch sections
        pitch_sections = grid_view.find_all(['div'], class_=lambda x: x and x.startswith('pitch-'))
        for pitch_section in pitch_sections:
            cards_container = pitch_section.find('div', class_='cards-container')
            if cards_container:
                for card_div in cards_container.find_all('div'):  # Each card is in a div
                    card_name_div = card_div.find('div', class_='card-name')
                    if card_name_div:
                        card_text = card_name_div.get_text(strip=True)
                        decklist['cards'].append(card_text)