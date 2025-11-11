from nt import environ
import discord
from discord.ext import commands
import functions.preprocessing as PP
import os
from dotenv import load_dotenv
import bd.acces_bd as bd

load_dotenv()
token = os.getenv('TOKEN_BOT')

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
    prayer_list=PP.prayer_time()
    msg = "Vos prières auront lieu aujourd'hui à :"
    for prayer_time in prayer_list:
        msg += f"\n- {prayer_time}"
    await ctx.send(msg)

@bot.command()
async def register(ctx,ville=None,decalage=None):
    if ville is None or decalage is None:
        await ctx.send("Veuillez fournir une ville et un décalage en minutes. Exemple : !register Neuchatel 20")
        return
    users = []
    data = bd.select_all()
    for ligne in data:
        users.append(ligne[0])
    
    if ctx.author.name in users:
        await ctx.send("Vous êtes déjà enregistré. Utilisez la commande !city pour mettre ç jour la ville et ! gap pour mettre à jour le décalage du rappel")
    else:
        bd.insert_user(ctx.author.name,ville,decalage)
        PP.set_reminder_by_user(ctx.author.name,ville,decalage)
        await ctx.send(f"Enregistrement réussi pour la ville de {ville} avec un décalage de {decalage} minutes.")

@bot.command()
async def city(ctx,new_ville=None):
    if new_ville is None:
        await ctx.send("Veuillez fournir une nouvelle ville. Exemple : !city Paris")
        return
    users = []
    data = bd.select_all()
    for ligne in data:
        users.append(ligne[0])
    if ctx.author.name not in users:
        await ctx.send("Vous n'êtes pas encore enregistré. Utilisez la commande !register pour vous enregistrer.")
    else:
        bd.update_ville(ctx.author.name,new_ville)
        PP.set_reminder_by_user(ctx.author.name,new_ville,decalage)
        await ctx.send(f"Enregistrement réussi pour la ville de {new_ville}")

@bot.command()
async def gap(ctx,new_decalage=None):
    if new_decalage is None:
        await ctx.send("Veuillez fournir un nouveau décalage en minutes. Exemple : !gap 15")
        return
    users = []
    data = bd.select_all()
    for ligne in data:
        users.append(ligne[0])
    if ctx.author.name not in users:
        await ctx.send("Vous n'êtes pas encore enregistré. Utilisez la commande !register pour vous enregistrer.")
    else:
        bd.update_decalage(ctx.author.name,new_decalage)
        await ctx.send(f"Enregistrement réussi pour le décalage de {new_decalage} minutes.")
        



bot.run(token)