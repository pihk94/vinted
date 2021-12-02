"""A set of utils"""
import pathlib
import json
from urllib.parse import urlparse, parse_qs
from datetime import datetime, timedelta, timezone

import discord
import requests

from vinted.client.vinted import Vinted

BASE_URL = 'https://www.vinted.fr/vetements'
OPTIONAL_PARAMETERS = [
    "catalog_ids",
    "color_ids",
    "size_ids",
    "material_ids",
    "status_ids",
    "country_ids",
    "city_ids"
]
DIRECTORY = pathlib.Path().resolve() / "vinted"
CURRENCIES = {
    "EUR": "€",
    "USD": "$"
}


def parse_url(url: str) -> dict:
    """Parse search url from vinted to a dictionnary ready
        to use for vinted api.

    Args:
        url (str): Url of the vinted search

    Returns:
        dict: Parameters dictionnary for vinted API
    """
    # Get url params from query
    url_params = parse_qs(urlparse(url).query)
    # Build params dic
    params = {
        "search_text": url_params.get("search_text")[0],
        "brand_ids": url_params.get("brand_id[]")[0],
        "order": "newest_first",
    }
    # Add optional parameters to params
    for param in OPTIONAL_PARAMETERS:
        if url_params.get(param[:-1] + "[]"):
            params[param] = ",".join(url_params.get(param[:-1] + "[]"))
    if url_params.get("status[]"):
        params["status_ids"] = ",".join(url_params.get("status[]"))
    return params


def reverse_url(params: dict) -> str:
    """[summary]

    Args:
        params (dict): [description]

    Returns:
        str: [description]
    """
    new_params = {
        "search_text": params['search_text'],
        "order": "newest_first",
    }
    for key, value in params.items():
        if key not in ['search_text', 'order']:
            if key == 'status_ids':
                new_params["status[]"] = value.split(',')
            else:
                new_params[key.replace('ids', 'id[]')] = value.split(',')
    return requests.get(BASE_URL, params=new_params).url


def write_last_check(
        id: int,
        dt: datetime = datetime.now(),
        filename: str = f"{DIRECTORY}/data/last_check.json") -> None:
    """Write last check date of items

    Args:
        dt (datetime): [description]
        filename (str, optional): [description]. Defaults to "last_check.txt".
    """
    with open(filename, "r") as f:
        data = json.load(f)
    data[str(id)] = dt.strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, "w") as out:
        json.dump(data, out, indent=4)


def get_last_check(
        id: int,
        filename: str = f"{DIRECTORY}/data/last_check.json") -> datetime:
    with open(filename, "r") as f:
        data = json.load(f)
    if data.get(str(id)) is None:
        dt = datetime.strptime(data[str(id)], "%Y-%m-%d %H:%M:%S")
    else:
        dt = datetime.now()
    return dt


def add_items(
        params: dict,
        filename: str = f"{DIRECTORY}/data/saved_searches.txt") -> None:
    """Add params of the search to file

    Args:
        params (dict): parsed params for search
        filename (str, optional): Filename where to write.
            Defaults to "saved_searches.txt".
    """
    with open(filename, "a") as f:
        f.write(f"{params}\n")


def create_embed(
        title: str,
        url: str,
        description: str,
        img_url: str,
        price: str,
        size: str,
        currency: str,
        status: str) -> discord.Embed:
    description = f"""
        **Taille**
            {size}
        **Description**
            {description}
        **Prix**
            {price}{CURRENCIES[currency]}
        **Condition**
            {status}
    """
    embed = discord.Embed(
        title=title,
        url=url,
        description=description,
        color=0x109319,
    )
    embed.set_image(
        url=img_url
    )
    return embed


def get_items(params: dict, id: int) -> list:
    """Get all items from vinted api

    Args:
        params (dict): Params of the vinted API search

    Returns:
        list: List of new items
    """
    # Create vinted client
    client = Vinted()
    # Get requests results
    response = client.get(
        endpoint="items",
        params=params
    )
    response.raise_for_status()
    # Get last date of results
    last_check = get_last_check(id=id).replace(
        tzinfo=timezone(timedelta(seconds=3600))
    )
    lst = []
    for i, item in enumerate(response.json()["items"]):
        if i == 0:
            first_time_date = datetime.fromisoformat(item.get("created_at_ts"))
        dt = datetime.fromisoformat(item.get("created_at_ts"))
        if dt > last_check:
            lst.append(
                {
                    "id": item.get("id"),
                    "title": item.get("title"),
                    "size": item.get("size"),
                    "price": item.get("price_numeric"),
                    "currency": item.get("currency"),
                    "condition": item.get("status"),
                    "description": item.get("description"),
                    "url": item.get("url"),
                    "img_url": item.get('photos')[0].get('url')
                }
            )
    if first_time_date < last_check:
        first_time_date = last_check
    return (lst, first_time_date)
