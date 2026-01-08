import discord
from discord.ext import commands, tasks
import random
import asyncio
import datetime
import os
import sys
from datetime import timedelta
from dotenv import load_dotenv

# --- CONFIGURATION & SECURITY ---
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
AUTHORIZED_USER = "luisthegoat7301"

if not TOKEN:
    print("ERROR: Token not found! Make sure you have a .env file with DISCORD_TOKEN inside.")
    exit()

PREFIX = '!'

# --- SETUP ---
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

# --- NATURE STATUS LOOP ---
nature_scenes = [
    "Beautiful Nature 🌲", "the Sunset 🌅", "Flowing Rivers 🌊",
    "Mountain Peaks 🏔️", "Starry Nights 🌌", "Blooming Flowers 🌸",
    "Falling Rain 🌧️", "the Forest 🦌"
]

@tasks.loop(seconds=60)
async def change_status():
    activity = discord.Activity(type=discord.ActivityType.watching, name=random.choice(nature_scenes))
    await bot.change_presence(status=discord.Status.dnd, activity=activity)

@change_status.before_loop
async def before_status():
    await bot.wait_until_ready()

# --- EVENTS ---
@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user.name} - ID: {bot.user.id}')
    print('✅ Connected to Discord!')
    print('------')
    change_status.start()

# --- ERROR HANDLING ---
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass 
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("⛔ **Access Denied:** You do not have the required permissions.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"⚠️ **Missing Argument:** Check command usage.")
    else:
        print(f"Error: {error}")

# ==============================================================================
# NEW SECTION: BOT CONTROL COMMANDS
# ==============================================================================

@bot.command()
async def start(ctx):
    """Starts/Signals the bot is active"""
    await ctx.send("🌲 **NatureBot is online and patrolling the forest!**")

@bot.command()
async def kill(ctx):
    """Exits the python code entirely"""
    if str(ctx.author) != AUTHORIZED_USER:
        return await ctx.send("⛔ Only Luisthegoat7301 can shut me down.")
    await ctx.send("💤 Powering down... Goodbye.")
    await bot.close()
    sys.exit()

@bot.command()
async def restart(ctx):
    """Pretends to restart with status changes"""
    if str(ctx.author) != AUTHORIZED_USER:
        return await ctx.send("⛔ Unauthorized.")
    change_status.stop()
    await bot.change_presence(status=discord.Status.invisible)
    msg = await ctx.send("🔄 **Restarting systems...**")
    await asyncio.sleep(5)
    await msg.edit(content="✅ **Systems rebooted.** Reconnecting to nature...")
    change_status.start()

@bot.command()
async def changeStatus(ctx, status_name: str):
    """Example: !changeStatus idle"""
    status_map = {
        "online": discord.Status.online,
        "idle": discord.Status.idle,
        "dnd": discord.Status.dnd,
        "invisible": discord.Status.invisible
    }
    choice = status_map.get(status_name.lower())
    if choice:
        change_status.stop() # Stop loop so it doesn't overwrite your manual choice
        await bot.change_presence(status=choice)
        await ctx.send(f"✅ Status updated to **{status_name}**.")
    else:
        await ctx.send("❌ Valid: online, idle, dnd, invisible")

@bot.command()
async def changePresence(ctx, p_type: str, *, text: str):
    """Example: !changePresence watching YouTube"""
    type_map = {
        "playing": discord.ActivityType.playing,
        "watching": discord.ActivityType.watching,
        "listening": discord.ActivityType.listening,
        "streaming": discord.ActivityType.streaming
    }
    act_type = type_map.get(p_type.lower())
    if act_type:
        change_status.stop()
        await bot.change_presence(activity=discord.Activity(type=act_type, name=text))
        await ctx.send(f"✅ Now {p_type} **{text}**.")
    else:
        await ctx.send("❌ Valid: playing, watching, listening, streaming")

@bot.command()
async def makerole(ctx, perm: str, *, name: str):
    """Owner command to create roles with perms"""
    if str(ctx.author) != AUTHORIZED_USER:
        return await ctx.send("⛔ Luisthegoat7301 access only.")
    
    perms = discord.Permissions.none()
    p = perm.lower()
    if p == "admin": perms = discord.Permissions(administrator=True)
    elif p == "ban": perms = discord.Permissions(ban_members=True)
    elif p == "kick": perms = discord.Permissions(kick_members=True)
    
    try:
        role = await ctx.guild.create_role(name=name, permissions=perms, color=discord.Color.random(), hoist=True)
        await ctx.send(f"✅ Created role **{role.name}** with **{p}** permissions!")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

# ==============================================================================
# SECTION 1: GENERAL COMMANDS
# ==============================================================================

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="🌿 NatureBot Help", description="Watching nature and moderating.", color=discord.Color.green())
    embed.add_field(name="Control", value="`start`, `restart`, `kill`, `changeStatus`, `changePresence`", inline=False)
    embed.add_field(name="General", value="`ping`, `serverinfo`, `userinfo`, `avatar`, `uptime`, `invite`, `poll`, `8ball`, `roll`, `coinflip`, `slap`, `hug`, `pat`, `kiss`, `ship`")
    embed.add_field(name="Moderation", value="`kick`, `ban`, `unban`, `softban`, `timeout`, `untimeout`, `purge`, `nuke`, `lock`, `unlock`, `slowmode`, `nick`, `addrole`, `removerole`, `warn`, `warnings`, `clearwarns`, `announce`, `dm`, `say`")
    embed.add_field(name="Cool/Custom", value="`hack`, `emojify`, `spoiler`, `reverse`, `mock`, `vaporwave`, `binary`, `morse`, `piglatin`, `advice`, `truth`, `dare`, `joke`, `iq`, `remindme`")
    await ctx.send(embed=embed)

@bot.command()
async def ping(ctx): await ctx.send(f'🏓 Pong! {round(bot.latency * 1000)}ms')

@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f"{guild.name} Info", color=discord.Color.blue())
    embed.add_field(name="Owner", value=guild.owner)
    embed.add_field(name="Members", value=guild.member_count)
    if guild.icon: embed.set_thumbnail(url=guild.icon.url)
    await ctx.send(embed=embed)

@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"{member.name}", color=member.color)
    embed.add_field(name="ID", value=member.id)
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"{member.name}'s Avatar")
    embed.set_image(url=member.avatar.url if member.avatar else member.default_avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def uptime(ctx): await ctx.send("I have been watching nature since I woke up!")

@bot.command()
async def invite(ctx):
    await ctx.send(f"Invite me: https://discord.com/oauth2/authorize?client_id={bot.user.id}&scope=bot&permissions=8")

@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title="📊 Poll", description=question, color=discord.Color.gold())
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("👍"); await msg.add_reaction("👎")

@bot.command(aliases=['8ball'])
async def eightball(ctx, *, question):
    responses = ["It is certain.", "Without a doubt.", "Ask again later.", "My sources say no."]
    await ctx.send(f"🎱 **Q:** {question}\n**A:** {random.choice(responses)}")

@bot.command()
async def roll(ctx, sides: int = 6): await ctx.send(f"🎲 Rolled a **{random.randint(1, sides)}**!")

@bot.command()
async def coinflip(ctx): await ctx.send(f"🪙 It's **{random.choice(['Heads', 'Tails'])}**!")

@bot.command()
async def slap(ctx, member: discord.Member):
    embed = discord.Embed(description=f"**{ctx.author.name}** slapped **{member.name}**!", color=discord.Color.red())
    embed.set_image(url="https://media.giphy.com/media/Gf3AUz3eBNb8q28W84/giphy.gif")
    await ctx.send(embed=embed)

@bot.command()
async def hug(ctx, member: discord.Member):
    embed = discord.Embed(description=f"**{ctx.author.name}** hugged **{member.name}**!", color=discord.Color.pink())
    embed.set_image(url="https://media.giphy.com/media/od5H3PmEG5EVq/giphy.gif")
    await ctx.send(embed=embed)

@bot.command()
async def pat(ctx, member: discord.Member): await ctx.send(f"**{ctx.author.name}** pats **{member.name}** on the head.")

@bot.command()
async def kiss(ctx, member: discord.Member): await ctx.send(f"😘 **{ctx.author.name}** kisses **{member.name}**!")

# ==============================================================================
# SECTION 2: MODERATION COMMANDS
# ==============================================================================

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="None"):
    await member.kick(reason=reason); await ctx.send(f"👢 Kicked {member}")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="None"):
    await member.ban(reason=reason); await ctx.send(f"🔨 Banned {member}")

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, user_id: int):
    user = await bot.fetch_user(user_id); await ctx.guild.unban(user); await ctx.send(f"🕊️ Unbanned {user}")

@bot.command()
@commands.has_permissions(ban_members=True)
async def softban(ctx, member: discord.Member):
    await member.ban(reason="Softban", delete_message_days=1); await member.unban(); await ctx.send(f"🧹 Softbanned {member}")

@bot.command()
@commands.has_permissions(moderate_members=True)
async def timeout(ctx, member: discord.Member, minutes: int):
    await member.timeout(timedelta(minutes=minutes)); await ctx.send(f"⏰ {member} timed out for {minutes}m.")

@bot.command()
@commands.has_permissions(moderate_members=True)
async def untimeout(ctx, member: discord.Member):
    await member.timeout(None); await ctx.send(f"🔊 Removed timeout for {member}")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int = 5):
    await ctx.channel.purge(limit=amount + 1); await ctx.send(f"🗑️ Deleted {amount} messages.", delete_after=3)

@bot.command()
@commands.has_permissions(administrator=True)
async def nuke(ctx):
    new = await ctx.channel.clone(); await ctx.channel.delete(); await new.send("💥 **Channel Nuked.**")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False); await ctx.send("🔒 Locked.")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True); await ctx.send("🔓 Unlocked.")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds); await ctx.send(f"🐢 Slowmode: {seconds}s.")

@bot.command()
@commands.has_permissions(manage_nicknames=True)
async def nick(ctx, member: discord.Member, *, name=None):
    await member.edit(nick=name); await ctx.send(f"🏷️ Changed nick for {member.name}")

@bot.command()
@commands.has_permissions(manage_roles=True)
async def addrole(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role); await ctx.send(f"✅ Added {role.name}")

@bot.command()
@commands.has_permissions(manage_roles=True)
async def removerole(ctx, member: discord.Member, role: discord.Role):
    await member.remove_roles(role); await ctx.send(f"❌ Removed {role.name}")

warnings = {}
@bot.command()
@commands.has_permissions(kick_members=True)
async def warn(ctx, member: discord.Member, *, r="No reason"):
    if member.id not in warnings: warnings[member.id] = []
    warnings[member.id].append(r); await ctx.send(f"⚠️ Warned {member.name}")

@bot.command()
async def warnings_list(ctx, member: discord.Member):
    w = warnings.get(member.id, [])
    await ctx.send(f"📋 {member.name} has {len(w)} warnings: {', '.join(w) if w else 'None'}")

@bot.command()
@commands.has_permissions(kick_members=True)
async def clearwarns(ctx, member: discord.Member):
    warnings[member.id] = []; await ctx.send(f"🧼 Cleared {member.name}")

@bot.command()
@commands.has_permissions(administrator=True)
async def announce(ctx, channel: discord.TextChannel, *, msg):
    await channel.send(embed=discord.Embed(title="📢 Announcement", description=msg, color=discord.Color.red()))

@bot.command()
@commands.has_permissions(administrator=True)
async def dm(ctx, member: discord.Member, *, msg):
    try: await member.send(f"📩 Staff: {msg}"); await ctx.send("Sent.")
    except: await ctx.send("DMs closed.")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def say(ctx, *, msg):
    await ctx.message.delete(); await ctx.send(msg)

# ==============================================================================
# SECTION 3: CUSTOM COOL COMMANDS
# ==============================================================================

@bot.command()
async def hack(ctx, member: discord.Member):
    m = await ctx.send(f"💻 Hacking {member.name}..."); await asyncio.sleep(1)
    await m.edit(content="...Stealing Wi-Fi..."); await asyncio.sleep(1)
    await m.edit(content="...Downloading homework..."); await asyncio.sleep(1)
    await m.edit(content=f"✅ {member.name} has been hacked.")

@bot.command()
async def emojify(ctx, *, text):
    res = "".join(f":regional_indicator_{c}: " if c.isalpha() else c for c in text.lower())
    await ctx.send(res)

@bot.command()
async def spoiler(ctx, *, text):
    await ctx.send("".join(f"||{c}||" for c in text))

@bot.command()
async def reverse(ctx, *, text): await ctx.send(text[::-1])

@bot.command()
async def mock(ctx, *, text):
    await ctx.send("".join(random.choice([c.upper(), c.lower()]) for c in text))

@bot.command()
async def vaporwave(ctx, *, text): await ctx.send(" ".join(text))

@bot.command()
async def binary(ctx, *, text):
    await ctx.send(f"```{' '.join(format(ord(c), '08b') for c in text)}```")

@bot.command()
async def morse(ctx, *, text):
    m_dict = {'A':'.-','B':'-...','C':'-.-.','D':'-..','E':'.','F':'..-.','G':'--.','H':'....','I':'..','J':'.---','K':'-.-','L':'.-..','M':'--','N':'-.','O':'---','P':'.--.','Q':'--.-','R':'.-.','S':'...','T':'-','U':'..-','V':'...-','W':'.--','X':'-..-','Y':'-.--','Z':'--..',' ':'/'}
    await ctx.send(" ".join(m_dict.get(c.upper(), c) for c in text))

@bot.command()
async def ship(ctx, m1: discord.Member, m2: discord.Member = None):
    m2 = m2 or ctx.author
    score = random.randint(0, 100)
    await ctx.send(f"❤️ **{m1.name}** x **{m2.name}**: {score}% compatible!")

@bot.command()
async def advice(ctx): await ctx.send(f"💡 {random.choice(['Drink water.', 'Sleep more.'])}")

@bot.command()
async def truth(ctx): await ctx.send(f"🤥 {random.choice(['Biggest fear?', 'Crush name?'])}")

@bot.command()
async def dare(ctx): await ctx.send(f"🔥 {random.choice(['Send last DM.', 'Meow in VC.'])}")

@bot.command()
async def joke(ctx): await ctx.send("🤣 Why did the bot cross the road? To get to the nature side!")

@bot.command()
async def iq(ctx): await ctx.send(f"🧠 IQ: **{random.randint(50, 200)}**")

@bot.command()
async def remindme(ctx, time: int, *, task):
    await ctx.send(f"⏰ Noted."); await asyncio.sleep(time); await ctx.send(f"🔔 {ctx.author.mention}: {task}")

# --- RUN ---
bot.run(TOKEN)