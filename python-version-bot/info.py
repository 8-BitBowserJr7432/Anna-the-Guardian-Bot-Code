import discord
from discord.ext import commands, tasks
import random
import asyncio
import os
import sys
import io
from dotenv import load_dotenv

# --- SETUP ---
load_dotenv()
TOKEN = os.getenv('INFO_BOT_TOKEN')
AUTHORIZED_USER = "luisthegoat7301"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# --- NATURE STATUS CYCLE ---
@tasks.loop(seconds=60)
async def nature_loop():
    scenes = ["Nature 🌲", "the Sunset 🌅", "Rivers 🌊", "Mountains 🏔️"]
    await bot.change_presence(status=discord.Status.dnd, 
                               activity=discord.Activity(type=discord.ActivityType.watching, name=random.choice(scenes)))

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user}')
    nature_loop.start()

# --- THE COMMAND (NOW FOR EVERYONE) ---
@bot.command()
async def htmlinfoForAnna(ctx):
    """Sends the HTML file with the Anna info link to ANY user who types it"""
    anna_link = "https://sites.google.com/view/info-about-anna?usp=sharing"
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ 
                background: #09090b; color: #ffffff; font-family: 'Segoe UI', sans-serif; 
                display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0;
            }}
            .card {{
                background: rgba(255, 255, 255, 0.05); border: 2px solid #22c55e;
                padding: 40px; border-radius: 15px; text-align: center;
                box-shadow: 0 0 30px rgba(34, 197, 94, 0.3);
                max-width: 400px;
            }}
            h1 {{ color: #22c55e; letter-spacing: 2px; margin-bottom: 10px; }}
            p {{ color: #a1a1aa; line-height: 1.6; }}
            .link-btn {{
                display: inline-block; margin-top: 25px; padding: 15px 30px;
                background: #22c55e; color: #000000; text-decoration: none;
                font-weight: bold; border-radius: 8px; transition: 0.3s;
                box-shadow: 0 4px 14px 0 rgba(34, 197, 94, 0.39);
            }}
            .link-btn:hover {{ 
                background: #4ade80; 
                transform: scale(1.05);
                box-shadow: 0 6px 20px rgba(34, 197, 94, 0.5);
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>ANNA INFO</h1>
            <p>You have requested the official information package for Anna.</p>
            <a href="{anna_link}" target="_blank" class="link-btn">GO TO SITE</a>
        </div>
    </body>
    </html>
    """
    
    # Send as an attachment
    file_data = io.BytesIO(html_content.encode('utf-8'))
    await ctx.send(
        content=f"📂 **Information Package Requested by {ctx.author.mention}**",
        file=discord.File(fp=file_data, filename="Anna_Info.html")
    )

# --- BOT CONTROL (STILL OWNER ONLY FOR SAFETY) ---
@bot.command()
async def kill(ctx):
    if str(ctx.author) == AUTHORIZED_USER:
        await ctx.send("💤 Process terminated.")
        await bot.close()
        sys.exit()

@bot.command()
async def restart(ctx):
    if str(ctx.author) == AUTHORIZED_USER:
        nature_loop.stop()
        await bot.change_presence(status=discord.Status.invisible)
        m = await ctx.send("🔄 Restarting...")
        await asyncio.sleep(5)
        await m.edit(content="✅ Systems Online.")
        nature_loop.start()

bot.run(TOKEN)