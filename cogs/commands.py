"""
:author: Shau
"""

import asyncio

import discord
from discord import app_commands, Embed, Forbidden, Status, ButtonStyle, Interaction
from discord.ui import View
from discord.ext import commands

from exceptions import Break


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def anunciar(self, ctx: commands.Context, *, mensagem: str) -> None:
        self.bot.logger.info(f"Comando: /anunciar {mensagem} por {ctx.author.name}")

        message = Embed(color=self.bot.color, description=mensagem)
        """
        cut_message = mensagem.split("\n")

        for line in cut_message:
            message.add_field(name=line, value="\u200b", inline=False)
            
            """

        class Buttons(View):
            def __init__(self, bot):
                super().__init__(timeout=None)

                self.bot = bot
                self.negar_button = self.children[0]
                self.confirmar_button = self.children[1]

            @discord.ui.button(label="Negar", style=ButtonStyle.danger)
            async def negar(self, interaction: Interaction, _: discord.ui.Button):
                await self.disable_buttons(interaction)

                await interaction.followup.send(
                    embed=Embed(color=self.bot.color, description="Anúncio cancelado"))

            @discord.ui.button(label="Confirmar", style=ButtonStyle.gray)
            async def confirmar(self, interaction: Interaction, _: discord.ui.Button):
                await self.disable_buttons(interaction)

                stop = False

                class StopButton(View):
                    def __init__(self):
                        super().__init__(timeout=None)

                        self.parar_button = self.children[0]

                    @discord.ui.button(label="Parar", style=ButtonStyle.danger)
                    async def parar(self, interaction: Interaction, _: discord.ui.Button):
                        await self.disable_buttons(interaction)

                        nonlocal stop
                        stop = True
                        await interaction.followup.send("Execução cancelada", ephemeral=True)

                    async def disable_buttons(self, interaction: Interaction):
                        self.parar_button.disabled = True
                        await interaction.response.edit_message(view=self)

                guild = interaction.guild
                await guild.chunk()

                response_message = await interaction.followup.send(embed=Embed(color=self.bot.color,
                                                                               description=f"Enviando anúncio para {members_online} usuários"),
                                                                   view=StopButton())

                counter = 0
                i = 0

                try:
                    for member in guild.members:
                        if stop:
                            raise Break

                        if i != 0:
                            embed = Embed(color=self.bot.color,
                                          description=f"Anúncio enviado para {counter} usuários")
                            embed.set_footer(
                                text=f"Essa mensagem é atualizada durante a execução do comando")

                            if i % 130 == 0:
                                for j in range(120, 0, -10):
                                    embed2 = Embed(color=self.bot.color,
                                                   description=f"Anúncio enviado para {counter} usuários")
                                    embed2.set_footer(
                                        text=f"Essa mensagem é atualizada durante a execução do comando\n\nAguardando {j} segundos para continuar a execução")
                                    try:
                                        await response_message.edit(embed=embed2)
                                    except Exception:
                                        print("Erro ao editar mensagem de atualização, tentando novamente depois do próximo delay...")

                                    seconds_counter = 0

                                    while seconds_counter < 10:
                                        await asyncio.sleep(1)
                                        seconds_counter += 1
                                        if stop:
                                            raise Break

                                try:
                                    await response_message.edit(embed=embed)
                                except Exception:
                                    print("Erro ao editar mensagem de atualização, tentando novamente depois do próximo delay...")
                            elif i % 10 == 0:
                                try:
                                    await response_message.edit(embed=embed)
                                except Exception:
                                    print("Erro ao editar mensagem de atualização, tentando novamente depois do próximo delay...")

                        if member == ctx.author or (member != self.bot.user and (
                                member.status == Status.online or member.status == Status.idle or member.status == Status.dnd or member.status == Status.do_not_disturb)):
                            try:
                                await member.send(embed=message)
                                counter += 1
                            except Exception:
                                pass

                            i += 1

                    await response_message.edit(embed=Embed(color=self.bot.color,
                                                            title=f"O anúncio foi enviado com sucesso para {counter} usuário{'s' if counter > 1 or counter == 0 else ''}")
                    .set_footer(
                        text=f"Alguns usuários podem não receber o anúncio por estarem com a DM desativada"),
                        view=None)

                except Break:
                    await response_message.edit(embed=Embed(color=self.bot.color,
                                                            title=f"O anúncio foi enviado com sucesso para {counter} usuário{'s' if counter > 1 or counter == 0 else ''}")
                    .set_footer(
                        text=f"Alguns usuários podem não receber o anúncio por estarem com a DM desativada\n\nExecução cancelada pelo usuário"),
                        view=None)

            async def disable_buttons(self, interaction: Interaction):
                self.negar_button.disabled = True
                self.confirmar_button.disabled = True
                await interaction.response.edit_message(view=self)

        members_online = sum(1 for member in ctx.guild.members if member == ctx.author or
                             ((
                                      member.status == Status.online or member.status == Status.idle or member.status == Status.dnd or member.status == Status.do_not_disturb)
                              and member != self.bot.user))

        await ctx.send(
            f"Você tem certeza que deseja enviar o seguinte anúncio para {members_online} usuário{'s' if members_online > 1 or members_online == 0 else ''}?",
            embed=message, view=Buttons(self.bot))

    async def cog_command_error(self, ctx: commands.Context, error: Exception) -> None:
        self.bot.logger.error(error)

        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send(embed=Embed(color=self.bot.color, title="Erro",
                                       description=f"Eu não tenho a(s) permissão(ões): {', '.join(error.missing_permissions)}"))
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(
                embed=Embed(color=self.bot.color, description="Você não tem permissão para executar isso!"))
        else:
            await ctx.send(embed=Embed(color=self.bot.color, title="Erro",
                                       description=f"{error.original}\n\n Por favor reporte para algum staff"))


async def setup(bot):
    await bot.add_cog(Commands(bot))
