import discord
import asyncio
import requests
from dotenv import dotenv_values
from humanize import intcomma, intword


setup = False
msgid = 979032726185332746 # set setup to true if you dont have this
channelid = 979023636012867644 # set to the channel id you want to get updates to


client = discord.Client()


@client.event
async def on_ready():
    print(f"Logged in as {client.user}. Online on {len(client.guilds)} Server(s).")
    if setup:
        embed = discord.Embed(title="SiriCoin Network Stats", description="SiriCoin Statistics - updated every 30s.", color=discord.Color.green())
        msg = await client.get_channel(channelid).send(embed = embed)
        print("Setup complete. Message id:", msg.id)
        raise SystemExit

async def update_stats():
    await client.wait_until_ready()
    while not client.is_closed():
        try:
            json = requests.get("https://node-1.siricoin.tech:5006/stats").json()
            embed = discord.Embed(title="SiriCoin Network Stats", description="SiriCoin Statistics - updated every 30s.", color=discord.Color.green())
            embed.add_field(name="Block count", value=intcomma(json["result"]["chain"]["length"]))
            embed.add_field(name="Difficulty", value=intword(int(json["result"]["chain"]["difficulty"])))
            embed.add_field(name="Holders", value=intcomma(json["result"]["coin"]["holders"]))
            embed.add_field(name="Supply", value=intcomma(json["result"]["coin"]["supply"]))
            embed.add_field(name="Transactions", value=intcomma(json["result"]["coin"]["transactions"]))
        except:
            embed = discord.Embed(title="SiriCoin Network Stats", description="Net down!", color=discord.Color.red())

        message = await client.get_channel(channelid).fetch_message(msgid)
        await message.edit(embed = embed)
        await asyncio.sleep(30)


if not setup:
    bg_task = client.loop.create_task(update_stats())

client.run(dotenv_values(".env")["TOKEN"])
