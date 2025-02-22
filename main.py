import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

async def carregar_cogs():
    for arquivo in os.listdir('cogs'):
        if arquivo.endswith('.py'):
            await bot.load_extension(f'cogs.{arquivo[:-3]}')

@bot.command()
async def sincronizar(ctx:commands.Context): 
    if ctx.author.id == 436857594871676940:
        alphacaard_server = discord.Object(id=1329817354711863358)
        sincs = await bot.tree.sync()
        await ctx.send(f"{len(sincs)} comandos sincronizados.")
    else:
        await ctx.reply('Apenas o criador pode usar esse comando.')
        return

@bot.command()
async def status(ctx:commands.Context):
    if ctx.author.id == 436857594871676940:
        await bot.change_presence(status=discord.Status.idle,activity=discord.Activity(type=discord.ActivityType.watching, name='você'))
        await ctx.send(f"Os status foram atualizados.")
    else:
        await ctx.reply('Apenas o criador pode usar esse comando.', ephemeral=True)
        return

@bot.tree.command(description='Responde o usuário com "Olá" ')
async def ola(interact:discord.Interaction):
    await interact.response.send_message(f'Olá, **{interact.user.mention}**!', ephemeral=True)
    
@bot.tree.command(description='Repete a mensagem enviada pelo usuário')
async def falar(interact:discord.Interaction, mensagem:str):
    await interact.response.send_message(mensagem)

@bot.event
async def on_ready():
    await carregar_cogs()
    print('Alphacaard está pronto!')

@bot.event
async def on_member_join(membro:discord.Member):
    canal = bot.get_channel(1332442749198405794)
    meu_embed = discord.Embed(title=f'▸ {membro.display_name} entrou no servidor!', 
                              description=f"> Seja bem-vindo(a).\n")
    meu_embed.set_thumbnail(url=membro.avatar)
    meu_embed.color = discord.Color.from_rgb(181, 193, 215)
    await canal.send(embed=meu_embed)

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
bot.run(TOKEN)