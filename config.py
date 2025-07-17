import os
from dotenv import load_dotenv
from typing import List

# Load environment variables
load_dotenv()

TOURNAMENT_URL_1="https://fabtcg.com/en/coverage/national-championship-2025-singapore/results/"
TOURNAMENT_URL_2="https://fabtcg.com/en/coverage/national-championship-2025-taiwan/results/"
TOURNAMENT_URL_3="https://fabtcg.com/en/coverage/national-championship-2025-belgium/results/"
TOURNAMENT_URL_4="https://fabtcg.com/en/coverage/national-championship-2025-brazil/results/"
TOURNAMENT_URL_5="https://fabtcg.com/en/coverage/national-championship-2025-bulgaria/results/"
TOURNAMENT_URL_6="https://fabtcg.com/en/coverage/national-championship-2025-croatia/results/"
TOURNAMENT_URL_7="https://fabtcg.com/en/coverage/national-championship-2025-cyprus/results/"
TOURNAMENT_URL_8="https://fabtcg.com/en/coverage/national-championship-2025-france/results/"
TOURNAMENT_URL_9="https://fabtcg.com/en/coverage/national-championship-2025-indonesia/results/"
TOURNAMENT_URL_10="https://fabtcg.com/en/coverage/national-championship-2025-lithuania/results/"
TOURNAMENT_URL_11="https://fabtcg.com/en/coverage/national-championship-2025-luxembourg/results/"
TOURNAMENT_URL_12="https://fabtcg.com/en/coverage/national-championship-2025-netherlands/results/"
TOURNAMENT_URL_13="https://fabtcg.com/en/coverage/national-championship-2025-new-zealand/results/"
TOURNAMENT_URL_14="https://fabtcg.com/en/coverage/national-championship-2025-slovakia/results/"
TOURNAMENT_URL_15="https://fabtcg.com/en/coverage/national-championship-2025-united-kingdom/results/"
TOURNAMENT_URL_16="https://fabtcg.com/en/coverage/national-championship-2025-vietnam/results/"
TOURNAMENT_URL_17="https://fabtcg.com/en/coverage/national-championship-2025-australia/results/"
TOURNAMENT_URL_18="https://fabtcg.com/en/coverage/national-championship-2025-austria/results/"
TOURNAMENT_URL_19="https://fabtcg.com/en/coverage/national-championship-2025-estonia/results/"
TOURNAMENT_URL_20="https://fabtcg.com/en/coverage/national-championship-2025-finland/results/"
TOURNAMENT_URL_21="https://fabtcg.com/en/coverage/national-championship-2025-greece/results/"
TOURNAMENT_URL_22="https://fabtcg.com/en/coverage/national-championship-2025-hungary/results/"
TOURNAMENT_URL_23="https://fabtcg.com/en/coverage/national-championship-2025-hong-kong-region/results/"
TOURNAMENT_URL_24="https://fabtcg.com/en/coverage/national-championship-2025-ireland/results/"
TOURNAMENT_URL_25="https://fabtcg.com/en/coverage/national-championship-2025-italy/results/"
TOURNAMENT_URL_26="https://fabtcg.com/en/coverage/national-championship-2025-japan/results/"
TOURNAMENT_URL_27="https://fabtcg.com/en/coverage/national-championship-2025-latvia/results/"
TOURNAMENT_URL_28="https://fabtcg.com/en/coverage/national-championship-2025-malaysia/results/"
TOURNAMENT_URL_29="https://fabtcg.com/en/coverage/national-championship-2025-mexico/results/"
TOURNAMENT_URL_30="https://fabtcg.com/en/coverage/national-championship-2025-norway/results/"
TOURNAMENT_URL_31="https://fabtcg.com/en/coverage/national-championship-2025-philippines/results/"
TOURNAMENT_URL_32="https://fabtcg.com/en/coverage/national-championship-2025-poland/results/"
TOURNAMENT_URL_33="https://fabtcg.com/en/coverage/national-championship-2025-portugal/results/"
TOURNAMENT_URL_34="https://fabtcg.com/en/coverage/national-championship-2025-south-korea/results/"
TOURNAMENT_URL_35="https://fabtcg.com/en/coverage/national-championship-2025-spain/results/"
TOURNAMENT_URL_36="https://fabtcg.com/en/coverage/national-championship-2025-sweden/results/"
TOURNAMENT_URL_37="https://fabtcg.com/en/coverage/national-championship-2025-brunei/results/"
TOURNAMENT_URL_38="https://fabtcg.com/en/coverage/national-championship-2025-canada/results/"
TOURNAMENT_URL_39="https://fabtcg.com/en/coverage/national-championship-2025-denmark/results/"
TOURNAMENT_URL_40="https://fabtcg.com/en/coverage/national-championship-2025-czechia/results/"
TOURNAMENT_URL_41="https://fabtcg.com/en/coverage/national-championship-2025-germany-main-event/results/"
TOURNAMENT_URL_42="https://fabtcg.com/en/coverage/national-championship-2025-iceland/results/"
TOURNAMENT_URL_43="https://fabtcg.com/en/coverage/national-championship-2025-romania/results/"
TOURNAMENT_URL_44="https://fabtcg.com/en/coverage/national-championship-2025-slovenia/results/"
TOURNAMENT_URL_45="https://fabtcg.com/en/coverage/national-championship-2025-switzerland/results/"
TOURNAMENT_URL_46="https://fabtcg.com/en/coverage/national-championship-2025-thailand/results/"
TOURNAMENT_URL_47="https://fabtcg.com/en/coverage/ch-battle-hardened-2025-cc/results/"

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
TOURNAMENT_URLS = [
TOURNAMENT_URL_1,
TOURNAMENT_URL_2,
TOURNAMENT_URL_3,
TOURNAMENT_URL_4,
TOURNAMENT_URL_5,
TOURNAMENT_URL_6,
TOURNAMENT_URL_7,
TOURNAMENT_URL_8,
TOURNAMENT_URL_9,
    TOURNAMENT_URL_10,
TOURNAMENT_URL_11,
TOURNAMENT_URL_12,
TOURNAMENT_URL_13,
TOURNAMENT_URL_14,
TOURNAMENT_URL_15,
TOURNAMENT_URL_16,
TOURNAMENT_URL_17,
TOURNAMENT_URL_18,
TOURNAMENT_URL_19,
TOURNAMENT_URL_20,
TOURNAMENT_URL_21,
TOURNAMENT_URL_22,
TOURNAMENT_URL_23,
TOURNAMENT_URL_24,
TOURNAMENT_URL_25,
TOURNAMENT_URL_26,
TOURNAMENT_URL_27,
TOURNAMENT_URL_28,
TOURNAMENT_URL_29,
TOURNAMENT_URL_30,
TOURNAMENT_URL_31,
TOURNAMENT_URL_32,
TOURNAMENT_URL_33,
TOURNAMENT_URL_34,
TOURNAMENT_URL_35,
TOURNAMENT_URL_36,
TOURNAMENT_URL_37,
TOURNAMENT_URL_38,
TOURNAMENT_URL_39,
TOURNAMENT_URL_40,
TOURNAMENT_URL_41,
TOURNAMENT_URL_42,
TOURNAMENT_URL_43,
TOURNAMENT_URL_44,
TOURNAMENT_URL_45,
TOURNAMENT_URL_46,
TOURNAMENT_URL_47
]
# i = 1
# while True:
#     url = os.getenv(f'TOURNAMENT_URL_{i}')
#     if not url:
#         break
#     TOURNAMENT_URLS.append(url)
#     i += 1