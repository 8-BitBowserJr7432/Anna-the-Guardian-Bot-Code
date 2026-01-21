import discord
from discord.ext import commands
from discord import ui, app_commands
import asyncio
import platform
import socket
import psutil
import sys

# 1. Setup Intents (Required for bots to read messages and manage channels)
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

# 2. Define the bot
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print('Bot is ready to create channels!')



# --- LOGIN MODAL CLASS ---
class AdminLoginModal(ui.Modal, title='Admin Panel Login'):
    # Define the input boxes
    username_input = ui.TextInput(label='Username', placeholder='Enter username...', min_length=2)
    password_input = ui.TextInput(label='Password', placeholder='Enter password...', style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        # Check the credentials
        if self.username_input.value == "put_username" and self.password_input.value == "put_password!":
            await interaction.response.send_message("✅ Login Successful! Access Granted.", ephemeral=True)
            # You can call your setup functions here
        else:
            await interaction.response.send_message("❌ Invalid Credentials. Access Denied.", ephemeral=True)

# --- BUTTON VIEW CLASS ---
class LoginButtonView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label="Login to Admin Panel", style=discord.ButtonStyle.grey, emoji="🔐")
    async def login_button(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_modal(AdminLoginModal())

# --- THE BOT COMMANDS ---
@bot.command()
async def admin(ctx):
    """Trigger the login button"""
    view = LoginButtonView()
    await ctx.send("⚠️ This action requires authentication. Please click below:", view=view)



@bot.command()
@commands.has_permissions(administrator=True) # Only admins should run this
async def setup_gaming(ctx):
    """
    Creates a 'Gaming Chat' category and populates it with popular game channels.
    """
    
    # The list of games and their corresponding emojis
    # formatting: "Game Name": "Emoji"
    games_list = {
        "minecraft": "⛏️",
        "roblox": "🟥",
        "fortnite": "🚌",
        "valorant": "🎯",
        "league-of-legends": "⚔️",
        "grand-theft-auto": "🚗",
        "call-of-duty": "🔫",
        "overwatch": "🛡️",
        "apex-legends": "🧬",
        "rocket-league": "⚽",
        "among-us": "🚀",
        "genshin-impact": "✨",
        "counter-strike": "💣"
    }

    guild = ctx.guild

    try:
        await ctx.send("🔨 Starting server setup... Creating category 'Gaming Chat'.")
        print("Creating Gaming chat and channels...")

        # 1. Create the Category
        category = await guild.create_category("Gaming Chat")

        # 2. Create the Channels inside the category
        for game_name, emoji in games_list.items():
            # Format: {emoji} ┃{game_name}
            channel_name = f"{emoji}┃{game_name}"
            
            await guild.create_text_channel(channel_name, category=category)
            # Small delay to be safe with Discord API rate limits
            await asyncio.sleep(0.5) 

        await ctx.send(f"✅ Success! Created category **Gaming Chat** with {len(games_list)} channels.")

    except discord.Forbidden:
        await ctx.send("❌ Error: I do not have the **Manage Channels** permission.")
    except Exception as e:
        await ctx.send(f"❌ An error occurred: {e}")


@bot.command()
@commands.has_permissions(administrator=True)
async def secure_gaming(ctx):
    """
    Sets permissions for all channels in 'Gaming Chat':
    - Role ID 1370394998041874502: View, Send, Read History (ALLOWED)
    - @everyone: View, Send, Read History (DENIED)
    """
    print("Securing channels...")
    # 1. Define the Role ID and Category Name
    target_role_id = 1370394998041874502
    category_name = "Community Chat"
    
    # 2. Get the Role and Category objects
    guild = ctx.guild
    role = guild.get_role(target_role_id)
    
    # Find the category by name
    category = discord.utils.get(guild.categories, name=category_name)

    # Error handling if role or category doesn't exist
    if not role:
        await ctx.send(f"❌ Error: Could not find role with ID `{target_role_id}`.")
        return
    if not category:
        await ctx.send(f"❌ Error: Could not find category named '**{category_name}**'.")
        return

    await ctx.send(f"🔒 Locking down **{category_name}** for role **{role.name}**...")

    # 3. Define the Permissions
    # Permissions for the specific role (Allow)
    role_perms = discord.PermissionOverwrite(
        view_channel=True,
        send_messages=True,
        read_message_history=True
    )

    # Permissions for @everyone (Deny)
    everyone_perms = discord.PermissionOverwrite(
        view_channel=False,
        send_messages=False,
        read_message_history=False
    )

    # 4. Loop through all channels in the category and apply changes
    count = 0
    try:
        for channel in category.channels:
            # Set permissions for the specific role
            await channel.set_permissions(role, overwrite=role_perms)
            
            # Set permissions for @everyone
            await channel.set_permissions(guild.default_role, overwrite=everyone_perms)
            
            count += 1
            await asyncio.sleep(0.2) # Small delay to prevent rate limits

        await ctx.send(f"✅ Success! Updated permissions for **{count}** channels in **{category_name}**.")
        print("Channels secured!")

    except Exception as e:
        await ctx.send(f"❌ An error occurred while updating permissions: {e}")


@bot.command()
@commands.has_permissions(administrator=True)
async def setup_community(ctx):
    """
    Creates a 'Community Chat' category with standard channels 
    like general, off-topic, media, etc.
    """
    
    # 1. List of channels and their emojis
    # Format: "Channel Name": "Emoji"
    channels_list = {
        "other-general": "💬",
        "off-topic": "🪐",
        "other-media": "📸",
        "other-memes": "🐸",
        "other-bot-commands": "🤖",
        "other-introductions": "👋",
        "other-music": "🎵",
        "other-art": "🎨",
        "polls": "📊"
    }

    guild = ctx.guild

    try:
        await ctx.send("🔨 Setting up community channels...")

        # 2. Create the Category
        # You can change "Community Chat" to "General" or anything else
        category = await guild.create_category("Community Chat")

        # 3. Create the Channels inside the category
        for name, emoji in channels_list.items():
            # Format: {emoji} ┃{channel_name}
            channel_name = f"{emoji}┃{name}"
            
            await guild.create_text_channel(channel_name, category=category)
            # Small delay to respect Discord API limits
            await asyncio.sleep(0.5) 

        await ctx.send(f"✅ Success! Created **Community Chat** with {len(channels_list)} channels.")

    except discord.Forbidden:
        await ctx.send("❌ Error: I need the **Manage Channels** permission to do this.")
    except Exception as e:
        await ctx.send(f"❌ An error occurred: {e}")


@bot.command()
@commands.has_permissions(administrator=True)
async def create_staff_logs(ctx):
    """
    Finds the existing 'Staff channels' category and adds a private staff-logs channel.
    """
    guild = ctx.guild
    category_name = "Staff channels"
    channel_name = "📜┃staff-logs-2"

    # 1. Find the existing category
    category = discord.utils.get(guild.categories, name=category_name)

    if category is None:
        await ctx.send(f"❌ Error: I couldn't find a category named '**{category_name}**'. Please make sure the name matches exactly!")
        return

    try:
        # 2. Define private permissions
        # Deny @everyone from seeing it, Allow Administrator roles
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            guild.me: discord.PermissionOverwrite(view_channel=True) # Ensure bot can see it
        }

        # 3. Create the channel inside that category
        new_channel = await guild.create_text_channel(
            channel_name, 
            category=category, 
            overwrites=overwrites
        )

        await ctx.send(f"✅ Created {new_channel.mention} inside the **{category_name}** category.")
        print("Staff channel has been created successfully!")

    except discord.Forbidden:
        await ctx.send("❌ Error: I don't have permission to manage channels.")
        print("Bot does not have permission!")

    except Exception as e:
        await ctx.send(f"❌ An error occurred: {e}")
        print("An unexpected error happened!")



@bot.command()
async def consoleInfo(ctx):
    # 1. System & Bot Info
    print("User asked for system info and the message is now being sent...")
    await ctx.send(f"https://cdn.discordapp.com/attachments/1370665397308882954/1387333872240300143/IMG_1452.jpeg?ex=6961ffda&is=6960ae5a&hm=0ddafa98dea17fc190717c5130f71c8bd8db5bdc1826c25ff543375bf7552d0e")
    system_os = f"{platform.system()} {platform.release()}"
    bot_name = bot.user.name
    bot_id = bot.user.id
    
    # 2. Hardware Info (RAM & CPU)
    ram = psutil.virtual_memory()
    ram_total = f"{round(ram.total / (1024**3), 2)} GB"
    ram_usage = f"{ram.percent}%"
    
    cpu_usage = f"{psutil.cpu_percent(interval=1)}%"
    cpu_count = psutil.cpu_count(logical=True)

    # 3. Graphics (Note: General Python libraries have limited GPU support 
    # without specific drivers like NVIDIA's. We will mark as 'N/A' if not found)
    gpu_info = "N/A (Requires specific drivers)"

    # 4. WiFi & Network Info
    hostname = socket.gethostname()
    try:
        # This method finds the "main" IP used for the internet
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
    except Exception:
        ip_address = "Unable to fetch"

    # 5. Create the Embed
    embed = discord.Embed(title="🖥️ System Console Information", color=discord.Color.blue())
    embed.add_field(name="🤖 Bot Name", value=bot_name, inline=True)
    embed.add_field(name="🆔 Bot ID", value=f"`{bot_id}`", inline=True)
    embed.add_field(name="💻 OS", value=system_os, inline=False)
    
    embed.add_field(name="🧠 CPU Usage", value=f"{cpu_usage} ({cpu_count} Threads)", inline=True)
    embed.add_field(name="📟 RAM", value=f"{ram_usage} / {ram_total}", inline=True)
    embed.add_field(name="🎮 Graphics", value=gpu_info, inline=True)
    
    embed.add_field(name="🌐 Hostname", value=hostname, inline=True)
    embed.add_field(name="📍 WiFi IP", value=f"`{ip_address}`", inline=True)
    
    embed.set_footer(text=f"Requested by {ctx.author.name}")
    print("Messaged sended!")
    await ctx.send(embed=embed)



@bot.command()
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, seconds: int):
    """
    Sets the slowmode for all text channels within the 'Gaming Chat' category.
    Usage: !slowmode 10
    """
    category_name = "Community Chat"
    
    # 1. Find the Gaming Chat category
    category = discord.utils.get(ctx.guild.categories, name=category_name)

    if not category:
        return await ctx.send(f"❌ Could not find a category named '**{category_name}**'.")

    # 2. Loop through channels in that category
    updated_channels = []
    for channel in category.text_channels:
        try:
            await channel.edit(slowmode_delay=seconds)
            updated_channels.append(channel.name)
        except Exception as e:
            print(f"Failed to update {channel.name}: {e}")

    # 3. Confirmation message
    if updated_channels:
        status = f"set to **{seconds}s**" if seconds > 0 else "disabled"
        await ctx.send(f"✅ Slowmode {status} for **{len(updated_channels)}** channels in {category_name}.")
    else:
        await ctx.send(f"⚠️ No text channels were updated in {category_name}.")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def deleteC(ctx, channel_name: str):
    """
    Deletes a specific channel by name.
    Usage: !deleteC channel-name
    """
    # 1. Look for the channel
    channel = discord.utils.get(ctx.guild.channels, name=channel_name)

    if channel:
        try:
            await channel.delete()
            await ctx.send(f"✅ Deleted channel: **{channel_name}**")
        except discord.Forbidden:
            await ctx.send("❌ Error: I don't have permission to delete that channel.")
        except Exception as e:
            await ctx.send(f"❌ Error: {e}")
    else:
        await ctx.send(f"⚠️ Could not find a channel named '**{channel_name}**'.")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def deleteCA(ctx, *, category_name: str):
    """
    Deletes a Category AND all channels inside it.
    Usage: !deleteCA Gaming Chat
    """
    # 1. Look for the category
    category = discord.utils.get(ctx.guild.categories, name=category_name)

    if category:
        try:
            # 2. Delete all channels inside the category first
            for channel in category.channels:
                await channel.delete()
            
            # 3. Delete the category itself
            await category.delete()
            await ctx.send(f"🗑️ Deleted Category **{category_name}** and all its channels.")
            
        except discord.Forbidden:
            await ctx.send("❌ Error: I don't have permission to delete that category.")
        except Exception as e:
            await ctx.send(f"❌ Error: {e}")
    else:
        await ctx.send(f"⚠️ Could not find a category named '**{category_name}**'.")



# REPLACE 'YOUR_TOKEN_HERE' WITH YOUR ACTUAL BOT TOKEN
bot.run('MTM4NzQyODEyNDkyNDQ0NDc5Mw.GK3qb3.2fYynXubpOp9HkawCOCXv9Sj1rXgNxrTeeZTY0')