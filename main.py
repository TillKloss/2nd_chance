import nextcord
from nextcord.ext import commands
import os

intents = nextcord.Intents.all()
client = commands.Bot(command_prefix="adm", intents=intents)

guild_id = 1195696554875555861
role_id = 1195709974916116530
target_channel_id = 1262939927650500719
channel_id = 1249433154167508992

@client.event
async def on_ready():
    await client.loop.create_task(status_task())


async def status_task():
    await client.change_presence(activity=nextcord.Game("2nd Chance"), status=nextcord.Status.online)


if __name__ == "__main__":
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            try:
                client.load_extension(f"cogs.{filename[:-3]}")
                print(f"Loaded {filename}")
            except Exception as e:
                print(f"Failed to load {filename}: {e}")

def load_token():
    with open("token.txt") as f:
        token = f.read().strip()
    return token

client.run(load_token())
