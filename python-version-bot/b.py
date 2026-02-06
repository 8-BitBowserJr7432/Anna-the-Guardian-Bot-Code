import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))

intents = discord.Intents.default()
intents.members = True  # Needed to assign roles

bot = commands.Bot(command_prefix="!", intents=intents)

# Role IDs from your perks message
LEVEL_1_ROLE_ID = 1393288669992976474
LEVEL_2_ROLE_ID = 1447925761628700803
LEVEL_3_ROLE_ID = 1461995913282060463  # Disabled

class BoosterView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        # Level 1 button
        self.add_item(discord.ui.Button(
            label="Claim Level 1 Perks",
            style=discord.ButtonStyle.primary,
            emoji="<:Discord_Server_Boost:1432568399803846766>",
            custom_id="claim_level_1"
        ))
        # Level 2 button
        self.add_item(discord.ui.Button(
            label="Claim Level 2 Perks",
            style=discord.ButtonStyle.success,
            emoji="<:Discord_Server_Boost:1432568399803846766>",
            custom_id="claim_level_2"
        ))
        # Level 3 button (disabled)
        self.add_item(discord.ui.Button(
            label="Claim Level 3 Perks",
            style=discord.ButtonStyle.secondary,
            emoji="<:Discord_Server_Boost:1432568399803846766>",
            custom_id="claim_level_3",
            disabled=True
        ))

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")
    try:
        synced = await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
        print(f"Synced {len(synced)} commands.")
    except Exception as e:
        print(f"Error syncing commands: {e}")

@bot.tree.command(
    name="boosters",
    description="Send the server booster perks message",
    guild=discord.Object(id=GUILD_ID)
)
async def boosters(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🚀 Server Booster Perks 🚀",
        description="Thanks for boosting our server! Each boost level unlocks amazing perks. Claim your rewards and enjoy all the benefits! 🎉",
        color=discord.Color.purple()
    )

    # Level 1
    embed.add_field(
        name=f"Level 1 Booster <@&{LEVEL_1_ROLE_ID}>",
        value=(
            "🎨 **Custom Role**\n- Pick any color for your role\n- Hoist your role above members\n- Optional Booster-only badge icon\n\n"
            "💬 **Exclusive Hidden Channels**\n- 🔒 Booster Chat – private lounge\n- <:Discord_Server_Boost:1432568399803846766> Booster Media – flex pics & clips\n- 🔔 Sneak Peeks – upcoming features & leaks\n\n"
            "🌈 **Custom Name Colors**\n- Request RGB / gradient colors\n- Seasonal color themes (🔥 Halloween, ❄️ Winter, 💖 Valentine’s)\n\n"
            "⭐ **Recognition & Status**\n- Special Booster Tag in chat\n- 📌 Highlighted in #boosters\n- 🙌 Shout-outs for every boost\n\n"
            "🎁 **Bonus Rewards**\n- 🎂 Birthday role & announcement\n- 🎟 Extra entries in giveaways\n- 💎 Exclusive server items / currency\n- 🛠 Priority support & faster help\n\n"
            "⚡ **Server Power**\n- 📣 Help unlock higher server boost levels\n- 🎵 Higher music quality\n- 🖼 More emojis & stickers\n- 🚀 Better performance & features"
        ),
        inline=False
    )

    # Level 2
    embed.add_field(
        name=f"Level 2 Booster <@&{LEVEL_2_ROLE_ID}>",
        value=(
            "Includes all Level 1 perks, plus:\n"
            "🌟 **Extra Premium Add-Ons**\n- 🏆 Custom animated role icon\n- 🧩 Access to ultra-hidden channels\n- 🗂 Personal text or voice channel\n- 🤖 Custom bot command\n\n"
            "💬 **24/7 Support**\n- Get help anytime, always online"
        ),
        inline=False
    )

    # Level 3
    embed.add_field(
        name=f"Level 3 Booster <@&{LEVEL_3_ROLE_ID}>",
        value=(
            "Includes all Level 1 & 2 perks, plus:\n"
            "🚀 **Ultimate Boosting Experience**\n- Maximum server influence & perks\n- Exclusive high-level recognition\n- Early access to major server events"
        ),
        inline=False
    )

    embed.set_footer(text="Every booster helps power up the server, unlock more emojis, music quality, and premium features for everyone! 💖")

    await interaction.response.send_message(embed=embed, view=BoosterView(), ephemeral=False)

@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type != discord.InteractionType.component:
        return

    custom_id = interaction.data.get("custom_id")
    member = interaction.user
    guild = interaction.guild

    # Level 1 button: just says got your perks
    if custom_id == "claim_level_1":
        await interaction.response.send_message("✅ Got your perks!", ephemeral=True)

    # Level 2 button: gives role and says got your perks
    elif custom_id == "claim_level_2":
        role = guild.get_role(LEVEL_2_ROLE_ID)
        if role in member.roles:
            await interaction.response.send_message("You already have the role! ✅", ephemeral=True)
        else:
            await member.add_roles(role)
            await interaction.response.send_message("🎉 Got your perks! You now have the Level 2 Booster role!", ephemeral=True)

    # Level 3 button: disabled
    elif custom_id == "claim_level_3":
        await interaction.response.send_message("Level 3 perks are not available yet! ❌", ephemeral=True)

bot.run(TOKEN)
