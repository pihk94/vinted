import json
import os

from discord.ext import commands, tasks
from discord_components import ActionRow, Button, ButtonStyle

from vinted.utils.utils import (
    parse_url,
    reverse_url,
    write_last_check,
    create_embed,
    get_items,
    init_last_check
)
from vinted.config import (
    FINAL_TRANSACTION,
    SAVED_SEARCHES,
    LAST_CHECK,
    logger,
    CHANNEL,
    TOKEN
)
from vinted.utils.helpers import HELP_ADD_ITEMS, HELP_REMOVE_ITEMS

# Init last check
init_last_check()

bot = commands.Bot(command_prefix="!")


@bot.command(
    name="add_items",
    help=HELP_ADD_ITEMS)
async def _add_items(ctx, url: str):
    logger.info(f"Adding new items: {url}")
    params = parse_url(url)
    # Read params of previous searches
    with open(SAVED_SEARCHES, 'r') as f:
        lines = f.readlines()
    lines = [json.loads(line) for line in lines]
    searches = [
        (line.get("search_text"), line.get("brand_ids")) for line in lines
    ]
    lst = []
    for search in searches:
        if (params.get("search_text") ==  search[0] and # noqa
            params.get("brand_ids") == search[1]): # noqa
            lst.append(True)
        else:
            lst.append(False)
    if sum(lst) > 0:
        await ctx.send(f"""
            Watcher already exist for :
        Text: {params.get("search_text")}
        Brand: {params.get("brand_ids")}
        Full parameters of watcher is:
            {params}
        """)
    else:
        # Write to file searches
        with open(SAVED_SEARCHES, "a") as f:
            f.write(f"{json.dumps(params)}\n")
        await ctx.send(f"Added to watcher search : {params}")


@bot.command(
    name="remove_items",
    help=HELP_REMOVE_ITEMS
)
async def remove_items(ctx, id: int = None):
    logger.info(f"Removing item id: {id}")
    with open(SAVED_SEARCHES, 'r') as f:
        lines = f.readlines()
    if id is None:
        searches = ""
        for i, line in enumerate(lines):
            searches += f"""Search ID: {i}, URL: {reverse_url(
                json.loads(line)
            )}\n"""
        await ctx.send(f"List of saved items:\n{searches}")
        return
    el = json.loads(lines[id])
    lines.pop(id)
    txt = f"This search has been deleted : {reverse_url(el)}"
    with open(SAVED_SEARCHES, 'w') as f:
        f.write("".join(lines))
    with open(LAST_CHECK, "r") as f:
        data = json.load(f)
    data.pop(str(id))
    with open(LAST_CHECK, "w") as out:
        json.dump(data, out, indent=4)
    await ctx.send(txt)


@bot.command(name="clear_message")
async def clear(ctx):
    await ctx.channel.purge()


@tasks.loop(minutes=3)
async def check_items():
    # Get all items that are watchlisted
    with open(SAVED_SEARCHES, 'r') as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        search = json.loads(line)
        items, first_time_date = get_items(search, i)
        for item in items:
            logger.info(f"Got {len(items)} items for {search}")
            embed = create_embed(
                item.get("title"),
                item.get("url"),
                item.get("description"),
                item.get("img_url"),
                item.get("price"),
                item.get("size"),
                item.get("currency"),
                item.get("status")
            )
            url_buy = f"{FINAL_TRANSACTION}{item.get('id')}"
            channel = bot.get_channel(CHANNEL)
            await channel.send(embed=embed, components=ActionRow([
                Button(
                    label="???? D??tails",
                    style=ButtonStyle.URL,
                    custom_id="1",
                    url=item.get("url")
                ),
                Button(
                    label="???? Acheter",
                    style=ButtonStyle.URL,
                    custom_id="2",
                    url=url_buy
                )
            ]))
        logger.info(f"Writing {first_time_date} for {search}")
        write_last_check(i, first_time_date)


@bot.event
async def on_ready():
    check_items.start()

bot.run(TOKEN)
