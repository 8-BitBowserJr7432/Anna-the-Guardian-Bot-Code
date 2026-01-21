import discord
from discord.ext import commands
import json
import os

# --- CONFIGURATION ---
TOKEN = 'MTM4ODkwMTU4NjA4ODEwNDAwOA.GRbqEl.DuwC_BFRS08a1hC_4dFpMYkTZXMlCb8bIqnJqw'  # <--- Paste your Bot Token here
DATA_FILE = "roblox_data.json"

# --- SETUP INTENTS ---
intents = discord.Intents.default()
intents.message_content = True 

bot = commands.Bot(command_prefix="!", intents=intents)

# --- DATA HANDLING ---
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ==========================================
# PART 1: ROBLOX PROFILE SETUP (From before)
# ==========================================

class RobloxProfileModal(discord.ui.Modal, title="Roblox Profile Setup"):
    rblx_display = discord.ui.TextInput(label="Display Name", placeholder="e.g. CoolGamer123", max_length=50)
    rblx_username = discord.ui.TextInput(label="Username", placeholder="e.g. @coolgamer_official", max_length=50)
    rblx_pfp = discord.ui.TextInput(label="Profile Picture URL", placeholder="https://i.imgur.com/...", required=False)
    rblx_robux = discord.ui.TextInput(label="How many Robux?", placeholder="e.g. 1500", max_length=8)

    async def on_submit(self, interaction: discord.Interaction):
        user_data = load_data().get(str(interaction.user.id), {})
        
        # Update profile data
        user_data.update({
            "display_name": self.rblx_display.value,
            "username": self.rblx_username.value,
            "pfp_url": self.rblx_pfp.value,
            "robux": self.rblx_robux.value
        })
        
        # Save complete DB
        db = load_data()
        db[str(interaction.user.id)] = user_data
        save_data(db)

        await interaction.response.send_message(f"✅ Profile saved!", ephemeral=True)

class SetupView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Setup Profile", style=discord.ButtonStyle.blurple, emoji="👤")
    async def open_setup(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(RobloxProfileModal())

# ==========================================
# PART 2: INVENTORY SYSTEM (7 Inputs split)
# ==========================================

# --- STEP 2 MODAL: COSTS & IMAGE ---
class InventoryStep2Modal(discord.ui.Modal, title="Step 2: Costs & Image"):
    def __init__(self, step1_data):
        super().__init__()
        self.step1_data = step1_data  # Carry over data from Step 1

    cost_1 = discord.ui.TextInput(label="Cost for Gamepass 1", placeholder="e.g. 100", max_length=10)
    cost_2 = discord.ui.TextInput(label="Cost for Gamepass 2", placeholder="e.g. 250", max_length=10)
    cost_3 = discord.ui.TextInput(label="Cost for Gamepass 3", placeholder="e.g. 500", max_length=10)
    img_url = discord.ui.TextInput(label="Inventory Image URL", placeholder="https://...", default="https://cdn.discordapp.com/attachments/1373287818243211325/1461336400988344381/roblox_ticket_icon.jpeg?ex=696a2f14&is=6968dd94&hm=a74c166226e7bfca37833648eec0c4d14c0d34a03f6c2e1a968b152d6ee64746")

    async def on_submit(self, interaction: discord.Interaction):
        # Merge Step 1 and Step 2 data
        inventory_data = {
            "gp1_id": self.step1_data['gp1'],
            "gp2_id": self.step1_data['gp2'],
            "gp3_id": self.step1_data['gp3'],
            "gp1_cost": self.cost_1.value,
            "gp2_cost": self.cost_2.value,
            "gp3_cost": self.cost_3.value,
            "inv_image": self.img_url.value
        }

        # Save to DB
        db = load_data()
        if str(interaction.user.id) not in db:
            db[str(interaction.user.id)] = {} # Create entry if they skipped !setup
        
        db[str(interaction.user.id)]["inventory"] = inventory_data
        save_data(db)

        await interaction.response.send_message("✅ Inventory setup complete! Use `!viewInventory` to see it.", ephemeral=True)

# --- INTERMEDIATE VIEW (BUTTON FROM STEP 1 TO STEP 2) ---
class ContinueToStep2View(discord.ui.View):
    def __init__(self, step1_data):
        super().__init__(timeout=300)
        self.step1_data = step1_data

    @discord.ui.button(label="Next Step: Add Prices", style=discord.ButtonStyle.green, emoji="➡️")
    async def go_next(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Open Modal 2
        await interaction.response.send_modal(InventoryStep2Modal(self.step1_data))

# --- STEP 1 MODAL: IDs ---
class InventoryStep1Modal(discord.ui.Modal, title="Step 1: Gamepass IDs"):
    gp1 = discord.ui.TextInput(label="Gamepass ID 1", placeholder="123456", max_length=20)
    gp2 = discord.ui.TextInput(label="Gamepass ID 2", placeholder="123456", max_length=20)
    gp3 = discord.ui.TextInput(label="Gamepass ID 3", placeholder="123456", max_length=20)

    async def on_submit(self, interaction: discord.Interaction):
        # Store data temporarily
        temp_data = {
            "gp1": self.gp1.value,
            "gp2": self.gp2.value,
            "gp3": self.gp3.value
        }
        # Ask user to click next (API limitation prevents opening Modal 2 directly)
        await interaction.response.send_message(
            "Ids Saved! Click below to finish setup.", 
            view=ContinueToStep2View(temp_data), 
            ephemeral=True
        )

# --- MAIN INVENTORY BUTTON ---
class InventoryStartView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Setup Inventory", style=discord.ButtonStyle.blurple, emoji="🎒")
    async def start_inv(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(InventoryStep1Modal())

# ==========================================
# COMMANDS
# ==========================================

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def setup(ctx):
    """Start profile setup"""
    embed = discord.Embed(title="Roblox Setup", description="Click to setup your Profile", color=discord.Color.blue())
    await ctx.send(embed=embed, view=SetupView())

@bot.command()
async def inventorySetup(ctx):
    """Start inventory setup"""
    embed = discord.Embed(title="Inventory Setup", description="Click to setup your Gamepasses (2 Steps).", color=discord.Color.green())
    await ctx.send(embed=embed, view=InventoryStartView())

@bot.command()
async def viewInventory(ctx, member: discord.Member = None):
    """Shows the user's Inventory"""
    if member is None: member = ctx.author
    
    db = load_data()
    user_id = str(member.id)
    
    if user_id not in db or "inventory" not in db[user_id]:
        await ctx.send("This user has not done inventory setup yet!")
        return

    inv = db[user_id]["inventory"]
    
    embed = discord.Embed(title=f"{member.display_name}'s Inventory", color=discord.Color.gold())
    
    # Add Gamepass Fields
    embed.add_field(name="🎫 Gamepass 1", value=f"**ID:** {inv['gp1_id']}\n**Cost:** {inv['gp1_cost']}", inline=True)
    embed.add_field(name="🎫 Gamepass 2", value=f"**ID:** {inv['gp2_id']}\n**Cost:** {inv['gp2_cost']}", inline=True)
    embed.add_field(name="🎫 Gamepass 3", value=f"**ID:** {inv['gp3_id']}\n**Cost:** {inv['gp3_cost']}", inline=True)
    
    # Set the specific image URL
    embed.set_image(url=inv['inv_image'])
    
    await ctx.send(embed=embed)

# 2. !rblxInfo Command (From before)
@bot.command()
async def rblxInfo(ctx, member: discord.Member = None):
    if member is None: member = ctx.author
    db = load_data()
    user_id = str(member.id)

    if user_id not in db or "username" not in db[user_id]:
        await ctx.send("This user has not done setup yet!")
        return

    data = db[user_id]
    embed = discord.Embed(title=f"{data['display_name']}'s Roblox Stats", color=discord.Color.red())
    embed.add_field(name="Username", value=data['username'], inline=True)
    embed.add_field(name="Robux Balance", value=f"R$ {data['robux']}", inline=True)
    if data['pfp_url'].startswith("http"):
        embed.set_thumbnail(url=data['pfp_url'])
    
    await ctx.send(embed=embed)

bot.run(TOKEN)