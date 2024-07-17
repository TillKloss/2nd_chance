import nextcord
from nextcord.ext import commands
import os

intents = nextcord.Intents.all()
client = commands.Bot(command_prefix="adm", intents=intents)

guild_id = 1147909103260274700
role_id = 1262926834811666462
target_channel_id = 1263124483477078036
channel_id = 1262946543183597721

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

client.run("MTI2Mjg3NTA2NzA1MDc1NDE4MQ.GC0vCa.1bVfxNSlf3tpEGJN4XVA2PfRyEkETIKN_S4jqQ")

"""
medaillons vor spielern in Announcment -------
@bewohner benachrichtigung -------
letzte 3 monate in channel anzeigen
#verwandelten channel farbe embed -------
profile pic -------------------
'kein spieler' wird nicht mit reingenommen -------------
"""