import discord
from discord.ext import commands, tasks
import random
import asyncio
import datetime
from datetime import timedelta
import os
from dotenv import load_dotenv

# --- CONFIGURATION & SECURITY ---
# Load variables from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Check if Token exists to prevent startup errors
if not TOKEN:
    print("ERROR: Token not found! Make sure you have a .env file with DISCORD_TOKEN inside.")
    exit()

PREFIX = '!'

# --- SETUP ---
# Enable all intents (Required for discord.py 2.0+)
# Make sure "Message Content Intent" and "Server Members Intent" are ON in Dev Portal
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

# --- EVENTS & STATUS ---
@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user.name} - ID: {bot.user.id}')
    print('✅ Connected to Discord!')
    print('------')
    change_status.start()

# Loop to change status every 60 seconds (Nature Theme)
@tasks.loop(seconds=60)
async def change_status():
    status_list = [
        "Beautiful Nature 🌲",
        "the Sunset 🌅",
        "Flowing Rivers 🌊",
        "Mountain Peaks 🏔️",
        "Starry Nights 🌌",
        "Blooming Flowers 🌸",
        "Falling Rain 🌧️",
        "the Forest 🦌"
    ]
    # Status=dnd (Red circle/Do Not Disturb)
    activity = discord.Activity(type=discord.ActivityType.watching, name=random.choice(status_list))
    await bot.change_presence(status=discord.Status.dnd, activity=activity)

@change_status.before_loop
async def before_status():
    await bot.wait_until_ready()

# --- ERROR HANDLING (Prevents crashes) ---
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        # Ignore unknown commands or send a small helper
        pass 
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("⛔ **Access Denied:** You do not have the required permissions to use this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"⚠️ **Missing Argument:** Please check the command usage.")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("⚠️ **I can't do that:** I am missing the necessary permissions on this server.")
    else:
        # Print other errors to console for debugging, but keep bot running
        print(f"Error: {error}")

# ==============================================================================
# SECTION 1: GENERAL COMMANDS (15) - Available to @everyone
# ==============================================================================

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="🌿 NatureBot Help", description="Watching nature and moderating.", color=discord.Color.green())
    embed.add_field(name="General", value="`ping`, `serverinfo`, `userinfo`, `avatar`, `uptime`, `invite`, `poll`, `8ball`, `roll`, `coinflip`, `slap`, `hug`, `pat`, `kiss`, `ship`")
    embed.add_field(name="Moderation", value="`kick`, `ban`, `unban`, `softban`, `timeout`, `untimeout`, `purge`, `nuke`, `lock`, `unlock`, `slowmode`, `nick`, `addrole`, `removerole`, `warn`, `warnings`, `clearwarns`, `announce`, `dm`, `say`")
    embed.add_field(name="Cool/Custom", value="`hack`, `emojify`, `spoiler`, `reverse`, `mock`, `vaporwave`, `binary`, `morse`, `piglatin`, `advice`, `truth`, `dare`, `joke`, `iq`, `remindme`")
    await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    await ctx.send(f'🏓 Pong! Latency: {round(bot.latency * 1000)}ms')

@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f"{guild.name} Info", color=discord.Color.blue())
    embed.add_field(name="Owner", value=guild.owner)
    embed.add_field(name="Members", value=guild.member_count)
    embed.add_field(name="Created At", value=guild.created_at.strftime("%Y-%m-%d"))
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    await ctx.send(embed=embed)

@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"{member.name}", color=member.color)
    embed.add_field(name="ID", value=member.id)
    embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d"))
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"{member.name}'s Avatar", color=discord.Color.purple())
    embed.set_image(url=member.avatar.url if member.avatar else member.default_avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def uptime(ctx):
    await ctx.send("I have been watching nature since I woke up!")

@bot.command()
async def invite(ctx):
    link = f"https://discord.com/oauth2/authorize?client_id={bot.user.id}&scope=bot&permissions=8"
    await ctx.send(f"Invite me to your forest! [Click Here]({link})")

@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title="📊 Poll", description=question, color=discord.Color.gold())
    embed.set_footer(text=f"Poll by {ctx.author}")
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")
    await msg.add.reaction("<:CarlBot_Birthday:1432568213085884428>")

@bot.command(aliases=['8ball'])
async def eightball(ctx, *, question):
    responses = ["It is certain.", "Without a doubt.", "Ask again later.", "My sources say no.", "Outlook not so good."]
    await ctx.send(f"🎱 **Question:** {question}\n**Answer:** {random.choice(responses)}")

@bot.command()
async def roll(ctx, sides: int = 6):
    await ctx.send(f"🎲 You rolled a **{random.randint(1, sides)}**!")

@bot.command()
async def coinflip(ctx):
    await ctx.send(f"🪙 It's **{'Heads' if random.choice([True, False]) else 'Tails'}**!")

@bot.command()
async def slap(ctx, member: discord.Member):
    gifs = ["https://media.giphy.com/media/Gf3AUz3eBNb8q28W84/giphy.gif", "https://media.giphy.com/media/xT9IgzFnSqzt2Sp3EI/giphy.gif"]
    embed = discord.Embed(description=f"**{ctx.author.name}** slapped **{member.name}**!", color=discord.Color.red())
    embed.set_image(url=random.choice(gifs))
    await ctx.send(embed=embed)

@bot.command()
async def hug(ctx, member: discord.Member):
    embed = discord.Embed(description=f"**{ctx.author.name}** hugged **{member.name}**!", color=discord.Color.pink())
    embed.set_image(url="https://media.giphy.com/media/od5H3PmEG5EVq/giphy.gif")
    await ctx.send(embed=embed)

@bot.command()
async def pat(ctx, member: discord.Member):
    await ctx.send(f"**{ctx.author.name}** gently pats **{member.name}** on the head. *There there...*")

@bot.command()
async def kiss(ctx, member: discord.Member):
    await ctx.send(f"😘 **{ctx.author.name}** gives **{member.name}** a big kiss!")

# ==============================================================================
# SECTION 2: MODERATION COMMANDS (20) - Restricted by Perms
# ==============================================================================

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.kick(reason=reason)
    await ctx.send(f"👢 **{member}** has been kicked. Reason: {reason}")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 **{member}** has been banned. Reason: {reason}")

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, user_id: int):
    user = await bot.fetch_user(user_id)
    await ctx.guild.unban(user)
    await ctx.send(f"🕊️ **{user}** has been unbanned.")

@bot.command()
@commands.has_permissions(ban_members=True)
async def softban(ctx, member: discord.Member, *, reason="Softban"):
    await member.ban(reason=reason, delete_message_days=1)
    await member.unban(reason="Softban unban")
    await ctx.send(f"🧹 **{member}** was softbanned (messages deleted, user kicked).")

@bot.command()
@commands.has_permissions(moderate_members=True)
async def timeout(ctx, member: discord.Member, minutes: int, *, reason="No reason"):
    duration = timedelta(minutes=minutes)
    await member.timeout(duration, reason=reason)
    await ctx.send(f"⏰ **{member}** has been timed out for {minutes} minutes.")

@bot.command()
@commands.has_permissions(moderate_members=True)
async def untimeout(ctx, member: discord.Member):
    await member.timeout(None, reason="Untimeout")
    await ctx.send(f"🔊 **{member}**'s timeout has been removed.")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int = 5):
    await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(f"🗑️ Deleted {amount} messages.")
    await asyncio.sleep(3)
    await msg.delete()

@bot.command()
@commands.has_permissions(administrator=True)
async def nuke(ctx):
    channel = ctx.channel
    pos = channel.position
    new_channel = await channel.clone()
    await channel.delete()
    await new_channel.edit(position=pos)
    await new_channel.send("💥 Channel nuked and re-created!")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 Channel locked.")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 Channel unlocked.")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"🐢 Slowmode set to {seconds} seconds.")

@bot.command()
@commands.has_permissions(manage_nicknames=True)
async def nick(ctx, member: discord.Member, *, nickname=None):
    await member.edit(nick=nickname)
    await ctx.send(f"🏷️ Nickname changed for **{member.name}**.")

@bot.command()
@commands.has_permissions(manage_roles=True)
async def addrole(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f"✅ Added **{role.name}** to **{member.name}**.")

@bot.command()
@commands.has_permissions(manage_roles=True)
async def removerole(ctx, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    await ctx.send(f"❌ Removed **{role.name}** from **{member.name}**.")

# Warning System (In-Memory)
warnings = {}

@bot.command()
@commands.has_permissions(kick_members=True)
async def warn(ctx, member: discord.Member, *, reason="No reason"):
    if member.id not in warnings:
        warnings[member.id] = []
    warnings[member.id].append(reason)
    await ctx.send(f"⚠️ **{member}** has been warned. Reason: {reason}")

@bot.command()
@commands.has_permissions(kick_members=True)
async def warnings(ctx, member: discord.Member):
    if member.id not in warnings or not warnings[member.id]:
        return await ctx.send(f"{member.name} has no warnings.")
    
    embed = discord.Embed(title=f"Warnings for {member.name}", color=discord.Color.orange())
    for i, warn in enumerate(warnings[member.id], 1):
        embed.add_field(name=f"Warning {i}", value=warn, inline=False)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(kick_members=True)
async def clearwarns(ctx, member: discord.Member):
    warnings[member.id] = []
    await ctx.send(f"🧼 Warnings cleared for **{member.name}**.")

@bot.command()
@commands.has_permissions(administrator=True)
async def announce(ctx, channel: discord.TextChannel, *, message):
    embed = discord.Embed(title="📢 Announcement", description=message, color=discord.Color.red())
    await channel.send(embed=embed)
    await ctx.send(f"Announcement sent to {channel.mention}")

@bot.command()
@commands.has_permissions(administrator=True)
async def dm(ctx, member: discord.Member, *, message):
    try:
        await member.send(f"📩 **Message from Server Staff:** {message}")
        await ctx.send(f"DM sent to {member.name}")
    except:
        await ctx.send("Could not DM this user (DMs closed).")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def say(ctx, *, message):
    await ctx.message.delete()
    await ctx.send(message)

# ==============================================================================
# SECTION 3: COOL CUSTOM COMMANDS (15+) - Logic & Games
# ==============================================================================

@bot.command()
async def hack(ctx, member: discord.Member):
    """Fake hack animation"""
    msg = await ctx.send(f"💻 Hacking **{member.name}**...")
    await asyncio.sleep(1)
    await msg.edit(content="...Fetching IP address... [192.168.0.1]")
    await asyncio.sleep(1)
    await msg.edit(content="...Stealing cookie recipe...")
    await asyncio.sleep(1)
    await msg.edit(content="...Downloading embarrassing photos...")
    await asyncio.sleep(1)
    await msg.edit(content=f"✅ HACK COMPLETE! **{member.name}** has been totally pwned.")

@bot.command()
async def emojify(ctx, *, text):
    output = ""
    for char in text.lower():
        if 'a' <= char <= 'z':
            output += f":regional_indicator_{char}: "
        elif char == ' ':
            output += "   "
        else:
            output += char
    await ctx.send(output)

@bot.command()
async def spoiler(ctx, *, text):
    output = "".join(f"||{char}||" for char in text)
    await ctx.send(output)

@bot.command()
async def reverse(ctx, *, text):
    await ctx.send(text[::-1])

@bot.command()
async def mock(ctx, *, text):
    output = "".join(random.choice([c.upper(), c.lower()]) for c in text)
    await ctx.send(f"🤡 {output}")

@bot.command()
async def vaporwave(ctx, *, text):
    output = " ".join(text)
    await ctx.send(output)

@bot.command()
async def binary(ctx, *, text):
    output = ' '.join(format(ord(char), '08b') for char in text)
    if len(output) > 2000:
        await ctx.send("Text too long to convert!")
    else:
        await ctx.send(f"```\n{output}\n```")

@bot.command()
async def morse(ctx, *, text):
    morse_dict = { 'A':'.-', 'B':'-...', 'C':'-.-.', 'D':'-..', 'E':'.', 'F':'..-.', 'G':'--.', 'H':'....', 'I':'..', 'J':'.---', 'K':'-.-', 'L':'.-..', 'M':'--', 'N':'-.', 'O':'---', 'P':'.--.', 'Q':'--.-', 'R':'.-.', 'S':'...', 'T':'-', 'U':'..-', 'V':'...-', 'W':'.--', 'X':'-..-', 'Y':'-.--', 'Z':'--..', '1':'.----', '2':'..---', '3':'...--', '4':'....-', '5':'.....', '6':'-....', '7':'--...', '8':'---..', '9':'----.', '0':'-----', ', ':'--..--', '.':'.-.-.-', '?':'..--..', '/':'-..-.', '-':'-....-', '(':'-.--.', ')':'-.--.-'}
    output = ' '.join(morse_dict.get(char.upper(), char) for char in text)
    await ctx.send(f"📡 `{output}`")

@bot.command()
async def piglatin(ctx, *, text):
    words = text.split()
    output = []
    for word in words:
        if word[0].lower() in 'aeiou':
            output.append(word + "yay")
        else:
            output.append(word[1:] + word[0] + "ay")
    await ctx.send(" ".join(output))

@bot.command()
async def ship(ctx, member1: discord.Member, member2: discord.Member = None):
    if not member2:
        member2 = ctx.author
    score = random.randint(0, 100)
    bar = "█" * (score // 10) + "░" * (10 - (score // 10))
    embed = discord.Embed(title="❤️ Love Calculator", description=f"**{member1.name}** x **{member2.name}**", color=discord.Color.magenta())
    embed.add_field(name="Compatibility", value=f"{score}% [{bar}]")
    if score > 90: msg = "True Love!"
    elif score > 50: msg = "Maybe..."
    else: msg = "Run away."
    embed.set_footer(text=msg)
    await ctx.send(embed=embed)

@bot.command()
async def advice(ctx):
    tips = ["Drink water.", "Don't eat yellow snow.", "Sleep is good.", "Be kind to yourself.", "Save your game frequently."]
    await ctx.send(f"💡 **Advice:** {random.choice(tips)}")

@bot.command()
async def truth(ctx):
    qs = ["What is your biggest fear?", "Who is your crush?", "What is the last lie you told?", "Have you ever peed in a pool?"]
    await ctx.send(f"🤥 **Truth:** {random.choice(qs)}")

@bot.command()
async def dare(ctx):
    dares = ["Send a screenshot of your last DM.", "Change your PFP for an hour.", "Type with your nose.", "Bark like a dog in voice chat."]
    await ctx.send(f"🔥 **Dare:** {random.choice(dares)}")

@bot.command()
async def joke(ctx):
    jokes = ["Why did the scarecrow win an award? Because he was outstanding in his field!", "I'm on a seafood diet. I see food and I eat it.", "Parallel lines have so much in common. It’s a shame they’ll never meet."]
    await ctx.send(f"🤣 {random.choice(jokes)}")

@bot.command()
async def iq(ctx):
    iq_score = random.randint(1, 200)
    msg = "Big Brain!" if iq_score > 150 else "Room temperature..." if iq_score < 80 else "Average."
    await ctx.send(f"🧠 Your IQ is **{iq_score}**. {msg}")

@bot.command()
async def remindme(ctx, time: int, *, task):
    await ctx.send(f"⏰ Reminder set for **{task}** in {time} seconds.")
    await asyncio.sleep(time)
    await ctx.send(f"⏰ **DING DING!** {ctx.author.mention}, don't forget: {task}")

# --- RUN BOT ---
bot.run(TOKEN)