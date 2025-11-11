from nt import environ
import discord
from discord.ext import commands
import preprocessing as PP

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Le bot \"{bot.user}\" a été démarré')

@bot.command()
async def status(ctx):
    print(f"Verification du status par un utilisateur . . .")
    await ctx.send("[🟢] En ligne")
    
@bot.command()
async def pray(ctx):
    print("ouiii")
    #await ctx.send(PP.prayer_adjust_time())

bot.run(environ.get("DISCORD_BOT_TOKEN"))   