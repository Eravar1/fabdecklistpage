import requests
from bs4 import BeautifulSoup
from db_handler import DatabaseHandler
from urllib.parse import urljoin
import logging
from psycopg2 import sql
from concurrent.futures import ThreadPoolExecutor

class TournamentScraper:
    BASE_DOMAIN = "https://fabtcg.com"
    
    def __init__(self):
        self.db = DatabaseHandler()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def scrape_tournament(self, tournament_url):
        """Main method to scrape a full tournament"""
        try:
            tournament_name = self._extract_tournament_name(tournament_url)
            
            max_rounds = self._determine_max_rounds(tournament_url)
            if not max_rounds:
                logging.warning(f"No rounds found for {tournament_name}")
                return
                
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = []
                for round_num in range(1, max_rounds + 1):
                    futures.append(executor.submit(
                        self._scrape_round,
                        tournament_url, round_num, tournament_name
                    ))
                
                for future in futures:
                    try:
                        future.result()
                    except Exception as e:
                        logging.error(f"Error processing round: {e}")
                        
            logging.info(f"Completed scraping {tournament_name}")
            
        except Exception as e:
            logging.error(f"Error scraping tournament {tournament_url}: {e}")
        # finally:
            # self.db.close()
            
    def _extract_tournament_name(self, url):
        """Extract tournament name from URL (matches your streamlit approach)"""
        parts = url.strip('/').split('/')
        # This matches how you process it in fab_streamlit.py:
        return parts[-2].replace('-', ' ').title()
        
    def _determine_max_rounds(self, base_url):
        """Determine how many rounds the tournament had"""
        for round_num in range(1, 20):  # Check up to 20 rounds
            round_url = f"{base_url}{round_num}/"
            response = self.session.head(round_url)
            if response.status_code != 200:
                return round_num - 1
        return None
        
    def _scrape_round(self, base_url, round_num, tournament_name):
        """Scrape a single round of the tournament"""
        round_url = f"{base_url}{round_num}/"
        try:
            response = self.session.get(round_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            matches = soup.find_all('div', class_='tournament-coverage__row--results')
            
            for match in matches:
                players = match.find_all('div', class_='tournament-coverage__player')
                if len(players) >= 2:
                    self._process_player(players[0], tournament_name)
                    self._process_player(players[1], tournament_name)
                    
        except Exception as e:
            logging.error(f"Error scraping round {round_num}: {e}")
            
    def _process_player(self, player_div, tournament_name):
        """Process player data with proper return value handling"""
        try:
            name = player_div.find('span').get_text(strip=True)
            hero_div = player_div.find('div', class_='tournament-coverage__player-hero-and-deck')
            hero = hero_div.get_text(strip=True).replace("View decklist", "").strip()
            
            decklist_link = hero_div.find('a', href=True)
            if not decklist_link:
                return
                
            decklist_url = urljoin(self.BASE_DOMAIN, decklist_link['href'])
            
            # Add or get player
            player_id = self.db.add_player(name)
            if player_id is None:
                # Player exists, get their ID
                player_id = self.db.get_player_id(name)
                if player_id is None:
                    raise ValueError(f"Failed to get ID for player {name}")
            
            # Add decklist
            self.db.add_decklist(player_id, tournament_name, hero, decklist_url)
            
        except Exception as e:
            logging.error(f"Error processing player {name}: {str(e)}")
            raise