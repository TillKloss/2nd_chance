import nextcord
from datetime import datetime
from nextcord.ext import commands
import pytz

german_tz = pytz.timezone('Europe/Berlin')


#---------TEST
guild_id = 11956965548755558611
embed_color = 0xffbb5c
target_channel_id = 1272315365409423420

voice_channels_test = {"Funk01 ":1272315108500050020,
                       "Funk02 ":1272315269808656386,
                       "Funk03 ":1272315290750816266,
                       "Funk04 ":1272315290750816266,
                       "Funk05 ":1272315290750816266,
                       "Funk06 ":1272315290750816266,
                       "Funk07 ":1272315290750816266,
                       "Funk08 ":1272315290750816266,
                       "Funk09 ":1272315290750816266,
                       "Funk10":1272315290750816266,
                       "Funk11":1272315290750816266,
                       "Funk12":1272315290750816266,
                       "Funk13":1272315290750816266,
                       "Funk14":1272315290750816266,
                       "Funk15":1272315290750816266,
                       "Funk16":1272315290750816266,
                       "Funk17":1272315290750816266,
                       "Funk18":1272315290750816266,
                       "Funk19":1272315290750816266,
                       "Funk20":1272315290750816266,
                       "Funk21":1272315290750816266,
                       "Funk22":1272315290750816266,
                       "Funk23":1272315290750816266,
                       "Funk24":1272315290750816266,
                       "Funk25":1272315290750816266}


"""
#---------PRODUCTION
guild_id = 1147909103260274700
embed_color = 0xffbb5c
target_channel_id = 1225560620880105575

voice_channels_test = {"Funk01 ":1198939632176480406,
                       "Funk02 ":1198939743744962560,
                       "Funk03 ":1198939922166448158,
                       "Funk04 ":1198940091792498708,
                       "Funk05 ":1198940202194960384,
                       "Funk06 ":1198940312635195492,
                       "Funk07 ":1198940412719665205,
                       "Funk08 ":1198940521641545790,
                       "Funk09 ":1198940633038078062,
                       "Funk10":1198940935808090202,
                       "Funk11":1198941190947606570,
                       "Funk12":1198941285915054100,
                       "Funk13":1198941387123589270,
                       "Funk14":1198941515226034307,
                       "Funk15":1198941598134837268,
                       "Funk16":1198941702136795187,
                       "Funk17":1198941815441739776,
                       "Funk18":1198941924611067955,
                       "Funk19":1198942019121324032,
                       "Funk20":1198942125727940689,
                       "Funk21":1198943168079605831,
                       "Funk22":1198943384761552897,
                       "Funk23":1198943277978759168,
                       "Funk24":1198943903651471410,
                       "Funk25":1198944052192755723}
"""


async def cleanup_channel(channel):
    messages = [msg async for msg in channel.history(limit=100)]
    for message in messages:
        await message.delete()


class VoiceChannelCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.voice_channels = voice_channels_test


    async def voice_buttons(self, channel):
        await cleanup_channel(self.client.get_channel(target_channel_id))

        view = nextcord.ui.View(timeout=None)
        for label, channel_id in self.voice_channels.items():
            button = VoiceChannelButton(channel_id=channel_id, label=label)
            view.add_item(button)

        await channel.send(embed=nextcord.Embed(title="Wähle einen Funk-Kanal:",
                                            color=embed_color), view=view)


    @commands.Cog.listener()
    async def on_ready(self):
        target_channel = self.client.get_channel(target_channel_id)
        if target_channel:
            await self.voice_buttons(target_channel)


class VoiceChannelButton(nextcord.ui.Button):
    def __init__(self, channel_id, label):
        super().__init__(label=label, style=nextcord.ButtonStyle.primary, custom_id=label)
        self.channel_id = channel_id

    async def callback(self, interaction):
        voice_channel = interaction.guild.get_channel(self.channel_id)
        if voice_channel is not None:
            await interaction.user.move_to(voice_channel)
            await interaction.response.send_message(embed=nextcord.Embed(
                title=f"Du wurdest in {voice_channel.name} verschoben.",
                color=embed_color).set_footer(text=datetime.now(german_tz).strftime('%d.%m.%Y %H:%M')), ephemeral=True)

        else:
            await interaction.response.send_message(embed=nextcord.Embed(
                title="Fehler: Funk-Kanal konnte nicht gefunden werden.",
                color=embed_color).set_footer(text=datetime.now(german_tz).strftime('%d.%m.%Y %H:%M')), ephemeral=True)


def setup(client):
    client.add_cog(VoiceChannelCog(client))
