import discord
from discord.ext import commands
from discord import ui
import asyncio
import platform
import socket
import psutil

# 1. Setup Intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

# 2. Define the Bot
bot = commands.Bot(command_prefix='!', intents=intents)

# --- LOGIN MODAL SYSTEM ---
class AdminLoginModal(ui.Modal, title='Admin Panel Login'):
    username_input = ui.TextInput(label='Username', placeholder='enter username')
    password_input = ui.TextInput(label='Password', placeholder='Password...', style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        if self.username_input.value == "Username" and self.password_input.value == "Password":
            await interaction.response.send_message("✅ **Login Successful!** You now have access to admin commands.", ephemeral=True)
        else:
            await interaction.response.send_message("❌ **Invalid Credentials.** Access Denied.", ephemeral=True)

class LoginButtonView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @ui.button(label="Login to Admin Panel", style=discord.ButtonStyle.grey, emoji="🔐")
    async def login_button(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_modal(AdminLoginModal())

# --- COMMANDS ---

@bot.event
async def on_ready():
    print(f'✅ Logged in as: {bot.user.name}')
    print(f'🆔 ID: {bot.user.id}')

@bot.command()
async def admin(ctx):
    """Trigger the Login Form"""
    await ctx.send("⚠️ This action requires authentication:", view=LoginButtonView())

@bot.command()
@commands.has_permissions(administrator=True)
async def consoleInfo(ctx):
    """System information display"""
    embed = discord.Embed(title="🖥️ System Console", color=discord.Color.blue())
    embed.add_field(name="OS", value=platform.system(), inline=True)
    embed.add_field(name="RAM Usage", value=f"{psutil.virtual_memory().percent}%", inline=True)
    embed.add_field(name="CPU", value=f"{psutil.cpu_percent()}%", inline=True)
    embed.add_field(name="IP", value=f"`{socket.gethostbyname(socket.gethostname())}`", inline=True)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def setup_gaming(ctx):
    """Create Gaming Category"""
    games = {"roblox": "🟥", "minecraft": "⛏️", "fortnite": "🚌"}
    category = await ctx.guild.create_category("Gaming Chat")
    for name, emoji in games.items():
        await ctx.guild.create_text_channel(f"{emoji}┃{name}", category=category)
    await ctx.send("✅ Gaming Category Created.")

# --- RUN THE BOT ---
bot.run('YOUR_BOT_TOKEN_HERE')