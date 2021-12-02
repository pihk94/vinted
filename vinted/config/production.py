"""Production config."""
import pathlib

DIRECTORY = pathlib.Path(__file__).parent.parent.resolve()
SAVED_SEARCHES = f"{DIRECTORY}/data/saved_searches.txt"
LAST_CHECK = f"{DIRECTORY}/data/last_check.json"
TRANSACTION_URL = "https://www.vinted.fr/transaction/buy/new"
BASE_PARAMS_TRANS = "?source_screen=item&transaction%5Bitem_id%5D="
FINAL_TRANSACTION = f"{TRANSACTION_URL}{BASE_PARAMS_TRANS}"
