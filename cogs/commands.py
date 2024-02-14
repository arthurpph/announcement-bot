"""
:author: Shau
"""

import asyncio

import discord
from discord import app_commands, Embed, Forbidden, HTTPException, Status
from discord.ext import commands


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def anunciar(self, ctx: commands.Context, *, mensagem: str) -> None:
        self.bot.logger.info(f"Comando: /anunciar {mensagem} by {ctx.author.name}")

        message = Embed(color=discord.Color.blue(), description=mensagem)

        guild = ctx.guild
        await guild.chunk()

        members_online = 0

        for member in guild.members:
            if member.status == Status.online:
                members_online += 1

        response_message = await ctx.send(
            embed=Embed(color=discord.Color.blue(), description=f"Enviando anúncio para {members_online} usuários"))

        counter = 0

        """
        for i in range(400):
            if i != 0:
                if i % 20 == 0:
                    for j in range(120, -1, -10):
                        embed = Embed(color=discord.Color.blue(),
                                      description=f"Anúncio enviado para {counter} usuários")
                        embed.set_footer(
                            text=f"Essa mensagem é atualizada durante a execução do comando\n\n Aguardando {j} segundos para continuar a execução")
                        await response_message.edit(embed=embed)
                        await asyncio.sleep(10)

                    embed = Embed(color=discord.Color.blue(),
                                  description=f"Anúncio enviado para {counter} usuários")
                    embed.set_footer(
                        text=f"Essa mensagem é atualizada durante a execução do comando")
                    await response_message.edit(embed=embed)

                elif i % 10 == 0:
                    embed = Embed(color=discord.Color.blue(), description=f"Anúncio enviado para {counter} usuários")
                    embed.set_footer(text="Essa mensagem é atualizada durante a execução do comando")
                    await response_message.edit(embed=embed)

            await ctx.author.send(embed=message)
            counter += 1

        """
        i = 0

        for member in guild.members:
            if i != 0:
                if i % 130 == 0:
                    for j in range(120, -1, -10):
                        embed = Embed(color=discord.Color.blue(),
                                      description=f"Anúncio enviado para {counter} usuários")
                        embed.set_footer(
                            text=f"Essa mensagem é atualizada durante a execução do comando\n\n Aguardando {j} segundos para continuar a execução")
                        await response_message.edit(embed=embed)
                        await asyncio.sleep(10)

                    embed = Embed(color=discord.Color.blue(),
                                  description=f"Anúncio enviado para {counter} usuários")
                    embed.set_footer(
                        text=f"Essa mensagem é atualizada durante a execução do comando")
                    await response_message.edit(embed=embed)
                elif i % 10 == 0:
                    embed = Embed(color=discord.Color.blue(), description=f"Anúncio enviado para {counter} usuários")
                    embed.set_footer(text="Essa mensagem é atualizada durante a execução do comando")
                    await response_message.edit(embed=embed)

            if member != ctx.author and member != self.bot.user and member.status == Status.online:
                try:
                    await member.send(embed=message)
                    counter += 1
                except Exception:
                    pass

            i += 1

        await response_message.edit(embed=Embed(color=discord.Color.blue(),
                                                title=f"O anúncio foi enviado com sucesso para todos os {counter} usuário{'s' if counter > 1 or counter == 0 else ''}"))

    async def cog_command_error(self, ctx: commands.Context, error: Exception) -> None:
        self.bot.logger.error(error)

        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send(embed=Embed(color=discord.Color.blue(), title="Erro",
                                       description=f"Eu não tenho a(s) permissão(ões): {', '.join(error.missing_permissions)}"))
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(
                embed=Embed(color=discord.Color.blue(), description="Você não tem permissão para executar isso!"))
        else:
            await ctx.send(embed=Embed(color=discord.Color.blue(), title="Erro",
                                       description=f"{error.original}\n\n Por favor reporte para algum staff"))


async def setup(bot):
    await bot.add_cog(Commands(bot))
