import json
import os
import asyncio
from datetime import datetime, timedelta
import nextcord
from nextcord.ext import commands


guild_id = 1147909103260274700
role_id = 1262926834811666462
target_channel_id = 1263124483477078036
channel_id = 1262946543183597721
embed_color = 0xffbb5c


class Vote(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.target_channel_id = target_channel_id
        self.channel_id = channel_id
        self.role_id = role_id
        self.votes_file = "votes.json"
        self.load_data()

    def load_data(self):
        if os.path.exists(self.votes_file):
            try:
                with open(self.votes_file, "r") as f:
                    data = json.load(f)
                    self.last_announcement = datetime.fromisoformat(data.get("last_announcement")) if data.get(
                        "last_announcement") else None
                    self.last_announcement_message = data.get("last_announcement_message")
                    self.message_ids = data.get("message_ids", [])
                    self.votes = data.get("votes", {})
            except (json.JSONDecodeError, IOError) as e:
                self.votes = {}
                self.last_announcement = None
                self.last_announcement_message = None
                self.message_ids = []
        else:
            self.votes = {}
            self.last_announcement = None
            self.last_announcement_message = None
            self.message_ids = []

    def save_data(self):
        data = {
            "votes": self.votes,
            "last_announcement": self.last_announcement.isoformat() if self.last_announcement else None,
            "last_announcement_message": self.last_announcement_message,
            "message_ids": self.message_ids
        }
        with open(self.votes_file, "w") as f:
            json.dump(data, f, indent=4)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.channel.id == channel_id:
            if "hat gerade für den Server" in message.content:
                player_name = message.content.split(" hat gerade für den Server")[0]

                if player_name in self.votes and player_name != "Ein Spieler":
                    self.votes[player_name] += 1
                elif player_name != "Ein Spieler":
                    self.votes[player_name] = 1
                self.save_votes()

    @nextcord.slash_command(name="topvoter", description="Zeigt die Top 3 Voter des Monats in einem Embed an.")
    async def slash_top_voter(self, ctx: commands.Context):
        await self.announce_top_voters()

    async def schedule_announcement(self):
        while True:
            now = datetime.now()
            if now.month != (now - timedelta(days=now.day)).month:
                if not self.last_announcement or self.last_announcement.month != now.month:
                    self.last_announcement = now
                    await self.announce_top_voters()
            await asyncio.sleep(1800)

    async def send_announcement(self, channel, embed, message_content):
        if await self.should_cleanup(channel):
            await self.cleanup_messages(channel)

        message = await channel.send(content=message_content, embed=embed)
        self.last_announcement_message = message.id
        self.message_ids.append(message.id)
        self.save_data()

    async def should_cleanup(self, channel):
        messages = [msg async for msg in channel.history(limit=100)]
        announcement_messages = [msg for msg in messages if msg.id in self.message_ids]
        return len(announcement_messages) >= 3

    async def cleanup_messages(self, channel):
        messages = [msg async for msg in channel.history(limit=100)]
        messages.reverse()
        announcement_messages = [msg for msg in messages if msg.id in self.message_ids]

        if len(announcement_messages) > 2:
            messages_to_delete = announcement_messages[:len(announcement_messages) - 2]
            for message in messages_to_delete:
                await message.delete()
                if message.id in self.message_ids:
                    self.message_ids.remove(message.id)

    async def announce_top_voters(self):
        top_voters = sorted(self.votes.items(), key=lambda x: (-x[1], x[0]))[:3]
        channel = self.client.get_channel(self.target_channel_id)

        if channel is None:
            return

        if top_voters:
            now = datetime.now()
            embed = nextcord.Embed(
                title=f"{now.strftime('%B')} | Top-Voter",
                description="Herzlichen Glückwunsch und vielen Dank für Eure Unterstützung!",
                color=embed_color
            )
            for idx, (name, votes) in enumerate(top_voters, start=1):
                if idx == 1:
                    place_emoji = ":first_place:"
                elif idx == 2:
                    place_emoji = ":second_place:"
                elif idx == 3:
                    place_emoji = ":third_place:"
                else:
                    place_emoji = ":medal:"

                embed.add_field(
                    name=f"{place_emoji} Platz {idx}: {name}",
                    value=f"Stimmen: {votes}",
                    inline=False
                )
            embed.set_footer(text=f"{now.strftime('%B')} {now.year} | {now.strftime('%d.%m.%Y %H:%M')} Uhr")

            role = channel.guild.get_role(role_id)
            if role:
                message_content = f"{role.mention}\n"
            else:
                message_content = ""

            await self.send_announcement(channel, embed, message_content)
        else:
            role = channel.guild.get_role(role_id)
            if role:
                message_content = f"{role.mention}\n"
            else:
                message_content = ""
            embed = nextcord.Embed(title="Diesen Monat wurden keine Stimmen vergeben.",
                                   color=embed_color)
            await self.send_announcement(channel, embed, message_content)

        self.reset_votes()
        self.save_votes()

    def reset_votes(self):
        for player in list(self.votes.keys()):
            if player != "last_announcement" and player != "last_announcement_message" and player != "message_ids":
                self.votes[player] = 0

    def load_votes(self):
        if os.path.exists(self.votes_file):
            try:
                with open(self.votes_file, "r") as f:
                    data = json.load(f)
                    self.last_announcement = datetime.fromisoformat(data.get("last_announcement")) if data.get(
                        "last_announcement") else None
                    self.last_announcement_message = data.get("last_announcement_message")
                    self.message_ids = data.get("message_ids", [])
                    self.votes = data.get("votes", {})
                    return self.votes
            except (json.JSONDecodeError, IOError) as e:
                return {}
        return {}

    def save_votes(self):
        data = {
            "votes": self.votes,
            "last_announcement": self.last_announcement.isoformat() if self.last_announcement else None,
            "last_announcement_message": self.last_announcement_message,
            "message_ids": self.message_ids
        }
        with open(self.votes_file, "w") as f:
            json.dump(data, f)


def setup(client):
    client.add_cog(Vote(client))
