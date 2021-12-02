"""Display search results, will be executed with a cron job."""
import json

from vinted.client.vinted import Vinted
from vinted.config.production import SAVED_SEARCHES
from vinted.utils.utils import get_last_check


def execute_script():
    client = Vinted()
    last_check = get_last_check()
    with open(SAVED_SEARCHES, 'r') as f:
        lines = f.readlines()
    searches = []
    for line in lines:
        search = json.loads(line)
        response = client.get(
            endpoint="items",
            params=search
        )
        response.raise_for_status()
        break



if __name__ == "main":
    execute_script()
