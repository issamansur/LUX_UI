import os
import datetime

import asyncio
import aiohttp
from vkpymusic import Service

from discord import (
    app_commands,
    utils,
    Client,
    Intents,
    Interaction,
    Object,
    Message,
    Status,
    ActivityType,
    Activity,
    Game,
    Streaming,
)

from discord.ext import commands

from cogs.source.actions import *
from cogs.source.answers import ANSWERS
from Settings import *

from cogs.Administration import Administration
from cogs.Voice import Voice
from cogs.Auth import Auth

SYNC_GUILD = Object(id=DEFAULT_GUILD_ID)


class SlashBot(commands.Bot):
    def __init__(self, *, command_prefix: str, intents: Intents):
        super().__init__(command_prefix=command_prefix, intents=intents)

    async def setup_hook(self):
        # set cogs
        await self.add_cog(Administration(client))
        await self.add_cog(Voice(client))
        await self.add_cog(Auth(client))
        # sync all
        """
        for server in client.guilds:
            self.tree.copy_global_to(guild=Object(id=server.id))
            await self.tree.sync(guild=Object(id=server.id))
        """
        # sync main
        self.tree.copy_global_to(guild=SYNC_GUILD)
        await self.tree.sync(guild=SYNC_GUILD)
        # on tree error
        self.tree.on_error = on_tree_error


client = SlashBot(command_prefix="/", intents=Intents.all())

# -------------------------------------------------------
activities = [
    Game(
        name="League of Legends",
    ),
    # ...
]


@client.event
async def on_ready():
    print(f"Has logged in as {client.user}")

    # set status
    await client.change_presence(
        status=Status.online,
        activity=activities[0],
    )

    # set services
    voice: Voice = client.get_cog("Voice")
    for guild in client.guilds:
        service: Service = Service.parse_config(rf"tokens/{guild.id}.ini")
        if service is not None:
            await voice.set_service(guild.id, service)
            print(f"\033[92mGuild {guild.name} connected!\033[0m")


"""
@app_commands.checks.cooldown(1, 30)
@client.tree.command(name="ping", description="Check bot")
async def _ping(interaction: Interaction):
    await interaction.response.send_message("Pong!")
"""


async def on_tree_error(interaction: Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        return await interaction.response.send_message(
            f"Command is currently on cooldown! Try again in **{error.retry_after:.2f}** seconds!"
        )

    elif isinstance(error, app_commands.CommandNotFound):
        print(error)

    else:
        raise error


@client.event
async def on_message(message: Message):
    if message.author == client.user:
        return

    text = message.content
    words = text.split()
    author = message.author
    channel = message.channel

    if f"<@{ADMIN_USER_ID}>" in text:
        await channel.send(f"<@{author.id}>, Владелец заблокировал функцию упоминания.")
        await message.delete()
        return

    if str(words[0]).lower() in actions:
        try:
            member = await client.fetch_user(words[1][2:-1])
            res = f"{author.display_name} {formatting(words[0])} {member.display_name} {' '.join(words[2:])}"
            await channel.send(content=res)
        except Exception as exception:
            await channel.send(f"Something went wrong: {exception}")
        return

    await client.process_commands(message)


# --------------------------------------------------------------------------


client.run(token=TOKEN)
