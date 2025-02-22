import discord
from discord import app_commands
from discord.ext import commands

class EmbedCriar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="criar_embed", description="Cria uma embed. Ordem: título, descrição e cor em hexadecimal!")
    @app_commands.describe(
        title="Título da embed",
        description="Descrição da embed",
        color="Cor da embed em hexadecimal (ex: #FF5733)"
    )
    async def embed(self, interaction: discord.Interaction, title: str, description: str, color: str):
        try:
            if color.startswith("#"):
                color = color[1:]
            color = int(color, 16)
        except ValueError:
            await interaction.response.send_message(
                "Por favor, forneça uma cor válida em hexadecimal (exemplo: #FF5733).",
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title=title,
            description=description,
            color=color
        )

        usuario = interaction.user
        avatar_url = usuario.avatar.url if usuario.avatar else usuario.default_avatar.url
        embed.set_footer(text=f"Criado por {usuario.display_name}", icon_url=avatar_url)

        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(EmbedCriar(bot))