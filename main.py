"""
:author: Shau
"""

import asyncio
import os
import platform
from typing import Final

import nest_asyncio
import discord
from discord import Intents, app_commands
from discord.ext import commands
from discord.ext.commands import Context, errors
from dotenv import load_dotenv

import logger

logger.load_logger()
load_dotenv()

TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")

intents: Intents = Intents.default()
intents.message_content = True  # NOQA
intents.presences = True  # NOQA
intents.members = True  # NOQA


class Bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix="/", intents=intents, help_command=None)

        self.logger = logger.get_logger()
        self.color = discord.Color.from_rgb(30, 30, 30)

    async def load_cogs(self) -> None:
        cogs = ["commands.py"]
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py") and filename in cogs:
                extension = filename[:-3]

                try:
                    await self.load_extension(f"cogs.{extension}")
                    self.logger.info(f"Extensão {filename} carregada com sucesso")
                except Exception as e:
                    exception = f"{type(e).__name__}: {e}"
                    self.logger.error(f"Falha ao carregar extensão {extension}\n{exception}")

    async def setup_hook(self) -> None:
        global synced

        self.logger.info(f"Logado como {bot.user}")

        await self.load_cogs()

        try:
            pass
        except Exception as e:
            exception = f"{type(e).__name__}: {e}"
            self.logger.error(f"Erro ao sincronizar os comandos: {exception}")

        self.logger.info(f"Sincronizado {0} comando{'s' if 0 > 1 or 0 == 0 else ''}")
        self.logger.info(f"Versão discord.py: {discord.__version__}")
        self.logger.info(f"Versão python: {platform.python_version()}")
        self.logger.info(
            f"Rodando em: {platform.system()} {platform.release()} ({os.name})"
        )


bot = Bot()
nest_asyncio.apply()
asyncio.run(bot.start(TOKEN))
