import discord
from discord import app_commands
from discord.ext import commands

class Calculos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()
    
    @app_commands.command()
    async def somar (self, interact:discord.Interaction, numero_1:float, numero_2:float):
        await interact.response.send_message(numero_1 + numero_2) 

async def setup(bot):
    await bot.add_cog(Calculos(bot))
