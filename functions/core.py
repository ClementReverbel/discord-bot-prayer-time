import discord
import asyncio
from discord import utils

async def handle_user_action(bot: discord.Client, user_id: int, sound_path: str):
    user = await bot.fetch_user(user_id)
    guilds = bot.guilds  # liste des serveurs où le bot est présent

    voice_channel = None

    for guild in guilds:
        # Essayer de récupérer le membre depuis l'API pour éviter les problèmes de cache
        member = None
        try:
            member = await guild.fetch_member(user_id)
        except discord.NotFound:
            # pas membre de ce guild
            continue
        except discord.Forbidden:
            # Pas la permission de fetcher les membres : retomber sur le cache
            member = guild.get_member(user_id)
        except Exception as e:
            print(f"Erreur en fetch_member pour guild {guild.id}: {e}")
            member = guild.get_member(user_id)

        if member and getattr(member, 'voice', None) and member.voice and member.voice.channel:
            voice_channel = member.voice.channel
            break

    if voice_channel:
        print(f"L'utilisateur {user.name} est dans le salon {voice_channel.name}")
        # Si le bot est déjà connecté dans ce guild, réutiliser la connexion
        existing_vc = utils.get(bot.voice_clients, guild=voice_channel.guild)
        if existing_vc and existing_vc.is_connected():
            vc = existing_vc
            try:
                await vc.move_to(voice_channel)
            except Exception:
                # si move_to échoue, on ignore et on utilise la connexion existante
                pass
        else:
            vc = await voice_channel.connect()
        
        # Jouer le son (doit être un fichier lisible par FFmpeg, ex: .mp3, .wav)
        vc.play(discord.FFmpegPCMAudio(sound_path))
        
        # Attendre la fin du son
        while vc.is_playing():
            await asyncio.sleep(1)
        
        await vc.disconnect()
        print(f"Son joué pour {user.name}")
    
    else:
        print(f"L'utilisateur {user.name} n'est pas en vocal, envoi d'un MP...")
        try:
            await user.send("Bouge ton cul. C'est l'heure de la prière.")
        except discord.Forbidden:
            print(f"Impossible d'envoyer un message à {user.name}")
