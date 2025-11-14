from nt import environ
import discord
from discord.ext import commands
import functions.preprocessing as PP
import os
from dotenv import load_dotenv
import functions.core as test
import bd.acces_bd as bd

load_dotenv()
token = os.getenv('TOKEN_BOT')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command('help')

@bot.event
async def on_ready():
    print(f'Le bot \"{bot.user}\" a été démarré')    
    PP.reset_reminders()
    bot.loop.create_task(PP.watch_times_forever(bot))
    

@bot.command()
async def status(ctx):
    print(f"Verification du status par un utilisateur . . .")
    await ctx.send("[🟢] En ligne")
    
@bot.command()
async def planning(ctx):
    ville=bd.get_ville_by_user(ctx.author.id)
    if ville is None:
        await ctx.send("Vous n'êtes pas encore enregistré. Utilisez la commande !register pour vous enregistrer.")
        return
    prayer_list=PP.prayer_time(ville=ville[0])
    msg = "Les horaires de vos prières auront lieu aujourd'hui à :"
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
    
    if str(ctx.author.id) in users:
        await ctx.send("Vous êtes déjà enregistré. Utilisez la commande !city pour mettre ç jour la ville et ! gap pour mettre à jour le décalage du rappel")
    else:
        bd.insert_user(ctx.author.id,ville,decalage)
        PP.set_reminder_by_user(ctx.author.id,ville,decalage)
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
    if str(ctx.author.id) not in users:
        await ctx.send("Vous n'êtes pas encore enregistré. Utilisez la commande !register pour vous enregistrer.")
    else:
        bd.update_ville(ctx.author.id,new_ville)
        decalage=bd.get_decalage_by_user(ctx.author.id)
        PP.set_reminder_by_user(ctx.author.id,new_ville,decalage[0])
        await ctx.send(f"Enregistrement réussi pour la ville de {new_ville}.")

@bot.command()
async def gap(ctx,new_decalage=None):
    if new_decalage is None:
        await ctx.send("Veuillez fournir un nouveau décalage en minutes. Exemple : !gap 15")
        return
    users = []
    data = bd.select_all()
    for ligne in data:
        users.append(ligne[0])
    if str(ctx.author.id) not in users:
        await ctx.send("Vous n'êtes pas encore enregistré. Utilisez la commande !register pour vous enregistrer.")
    else:
        bd.update_decalage(ctx.author.id,new_decalage)
        ville=bd.get_ville_by_user(ctx.author.id)
        PP.set_reminder_by_user(ctx.author.id,ville[0],new_decalage)
        await ctx.send(f"Enregistrement réussi pour le décalage de {new_decalage} minutes.")
        

@bot.command()
async def ping(ctx):
    await test.handle_user_action(bot,ctx.author.id,"sounds/notification.mp3")

@bot.command()
async def suppr(ctx):
    all_users = bd.select_all()
    if str(ctx.author.id) not in [str(user[0]) for user in all_users]:
        await ctx.send("Vous n'êtes pas encore enregistré. Utilisez la commande !register pour vous enregistrer.")
        return
    PP.remove_user(ctx.author.id)
    await ctx.send(f"Suppression de vos données réussie.")

@bot.command()
async def help(ctx):
    help_message = """
    Commandes disponibles :
    !status - Vérifie si le bot est en ligne.
    !planning - Affiche les horaires de prière pour aujourd'hui.
    !register <ville> <décalage> - Enregistre votre ville et le décalage en minutes pour les rappels de prière.
    !city <nouvelle_ville> - Met à jour votre ville enregistrée.
    !gap <nouveau_décalage> - Met à jour le décalage en minutes pour vos rappels de prière.
    !ping - Teste la fonctionnalité de notification du bot.
    !help - Affiche ce message d'aide.
    !suppr - Supprime vos données enregistrées.
    """
    await ctx.send(help_message)        
    
@bot.command()
async def profile(ctx):
    user_id = ctx.author.id
    ville = bd.get_ville_by_user(user_id)
    decalage = bd.get_decalage_by_user(user_id)
    
    if ville is None or decalage is None:
        await ctx.send("Vous n'êtes pas encore enregistré. Utilisez la commande !register pour vous enregistrer.")
        return
    
    profile_message = f"""
    Profil de l'utilisateur {ctx.author.name} :
    - Ville : {ville[0]}
    - Décalage des rappels : {decalage[0]} minutes
    """
    await ctx.send(profile_message)

bot.run(token)