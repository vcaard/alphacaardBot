import discord
from discord import app_commands
from discord.ext import commands
from datetime import timedelta

# Dicionário para armazenar avisos temporariamente
warnings_db = {}

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Comando para banir um usuário
    @app_commands.command(name="ban", description="Bane um usuário do servidor.")
    async def ban(self, interaction: discord.Interaction, member: discord.Member, motivo: str = "Sem motivo"):
        if not interaction.user.guild_permissions.ban_members:
            await interaction.response.send_message("❌ Você não tem permissão para banir membros.", ephemeral=True)
            return
        
        await member.ban(reason=motivo)
        await interaction.response.send_message(f"🔨 {member.mention} foi banido do servidor. Motivo: {motivo}")

    # Comando para desbanir um usuário
    @app_commands.command(name="unban", description="Desbane um usuário pelo username.")
    async def unban(self, interaction: discord.Interaction, username: str):
        if not interaction.user.guild_permissions.ban_members:
            await interaction.response.send_message("❌ Você não tem permissão para desbanir membros.", ephemeral=True)
            return

        banned_users = await interaction.guild.bans()
        for ban_entry in banned_users:
            user = ban_entry.user
            if f"{username}" == username:
                await interaction.guild.unban(user)
                await interaction.response.send_message(f"✅ {username} foi desbanido.")
                return
        
        await interaction.response.send_message("❌ Usuário não encontrado na lista de banidos.")

    # Comando para expulsar um usuário
    @app_commands.command(name="kick", description="Expulsa um usuário do servidor.")
    async def kick(self, interaction: discord.Interaction, member: discord.Member, motivo: str = "Sem motivo"):
        if not interaction.user.guild_permissions.kick_members:
            await interaction.response.send_message("❌ Você não tem permissão para expulsar membros.", ephemeral=True)
            return

        await member.kick(reason=motivo)
        await interaction.response.send_message(f"👢 {member.mention} foi expulso. Motivo: {motivo}")

    # Comando para mutar um usuário
    @app_commands.command(name="mute", description="Silencia um usuário por um tempo determinado.")
    async def mute(self, interaction: discord.Interaction, member: discord.Member, minutos: int = 10):
        if not interaction.user.guild_permissions.manage_roles:
            await interaction.response.send_message("❌ Você não tem permissão para silenciar membros.", ephemeral=True)
            return

        mute_role = discord.utils.get(interaction.guild.roles, name="Mutado")
        if not mute_role:
            mute_role = await interaction.guild.create_role(name="Mutado", reason="Criando cargo de mute")

            for channel in interaction.guild.channels:
                await channel.set_permissions(mute_role, send_messages=False)

        await member.add_roles(mute_role)
        await interaction.response.send_message(f"🔇 {member.mention} foi silenciado por {minutos} minutos.")

        await discord.utils.sleep_until(discord.utils.utcnow() + timedelta(minutes=minutos))
        await member.remove_roles(mute_role)
        await interaction.followup.send(f"🔊 {member.mention} foi desmutado automaticamente.")

    # Comando para desmutar um usuário
    @app_commands.command(name="unmute", description="Remove o silêncio de um usuário.")
    async def unmute(self, interaction: discord.Interaction, member: discord.Member):
        if not interaction.user.guild_permissions.manage_roles:
            await interaction.response.send_message("❌ Você não tem permissão para remover o mute.", ephemeral=True)
            return

        mute_role = discord.utils.get(interaction.guild.roles, name="Mutado")
        if mute_role and mute_role in member.roles:
            await member.remove_roles(mute_role)
            await interaction.response.send_message(f"🔊 {member.mention} foi desmutado.")
        else:
            await interaction.response.send_message("❌ Esse usuário não está silenciado.", ephemeral=True)

    # Comando para avisar um usuário
    @app_commands.command(name="warn", description="Dá um aviso para um usuário.")
    async def warn(self, interaction: discord.Interaction, member: discord.Member, motivo: str = "Sem motivo"):
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message("❌ Você não tem permissão para dar avisos.", ephemeral=True)
            return

        if member.id not in warnings_db:
            warnings_db[member.id] = []

        warnings_db[member.id].append(motivo)
        await interaction.response.send_message(f"⚠️ {member.mention} recebeu um aviso. Motivo: {motivo}")

    # Comando para ver os avisos de um usuário
    @app_commands.command(name="warnings", description="Mostra os avisos de um usuário.")
    async def warnings(self, interaction: discord.Interaction, member: discord.Member):
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message("❌ Você não tem permissão para ver avisos.", ephemeral=True)
            return

        avisos = warnings_db.get(member.id, [])
        if avisos:
            await interaction.response.send_message(f"📋 {member.mention} tem {len(avisos)} aviso(s):\n" + "\n".join(avisos))
        else:
            await interaction.response.send_message(f"✅ {member.mention} não tem avisos.")

async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))
