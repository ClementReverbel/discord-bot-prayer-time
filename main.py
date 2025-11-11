from nt import environ
import discord
from discord.ext import commands
import functions.preprocessing as PP

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
async def planning(ctx):
    prayer_list=PP.prayer_adjust_time()
    msg = "Vos prières auront lieu aujourd'hui :"
    for prayer_time in prayer_list:
        msg += f"\n- {prayer_time}"
    await ctx.send(msg)
    
@bot.command()
async def who(ctx):
    await ctx.send("Tu es " + ctx.author.mention)
    
@bot.command()
async def register(ctx,ville,decalage):
    await ctx.send("Fonction d'enregistrement non encore implémentée.")

bot.run(environ.get("DISCORD_BOT_TOKEN"))   