import os
from dotenv import load_dotenv
from typing import List

# Load environment variables
load_dotenv()

# Database configuration
DB_CONFIG = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

# Discord bot configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Team members (from comma-separated string)
TEAM_MEMBERS = [name.strip() for name in os.getenv('TEAM_MEMBERS', '').split(',') if name.strip()]

# Tournament URLs (collect all TOURNAMENT_URL_{n} variables)
TOURNAMENT_URLS = []
i = 1
while True:
    url = os.getenv(f'TOURNAMENT_URL_{i}')
    if not url:
        break
    TOURNAMENT_URLS.append(url)
    i += 1