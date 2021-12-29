import pathlib
import logging
import os

ENVS = ["production", "development"]

# Get environment
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

# Import the good config

if ENVIRONMENT == 'production':
    from config.production import *
elif ENVIRONMENT == "development":
    from config.development import *
elif ENVIRONMENT not in ENVS:
    raise ValueError(f"Environment must be in {ENVS}")

# Logger configuration
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log',
    encoding='utf-8',
    mode='w'
)
handler.setFormatter(
    logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s')
)
logger.addHandler(handler)

# Basic parameters
DIRECTORY = pathlib.Path(__file__).parent.parent.resolve()
SAVED_SEARCHES = f"{DIRECTORY}/data/saved_searches.txt"
LAST_CHECK = f"{DIRECTORY}/data/last_check.json"
TRANSACTION_URL = "https://www.vinted.fr/transaction/buy/new"
BASE_PARAMS_TRANS = "?source_screen=item&transaction%5Bitem_id%5D="
FINAL_TRANSACTION = f"{TRANSACTION_URL}{BASE_PARAMS_TRANS}"
