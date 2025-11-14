import discord
import asyncio
from nt import environ
import discord
from discord.ext import commands
import functions.preprocessing as PP
from discord import FFmpegOpusAudio, PCMVolumeTransformer, utils

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
            # Vérifier que le bot a la permission de se connecter et parler
            bot_member = voice_channel.guild.me
            perms = voice_channel.permissions_for(bot_member) if bot_member else None
            if perms and (not perms.connect or not perms.speak):
                print(f"Le bot n\'a pas la permission de se connecter/parler dans {voice_channel.name} (guild {voice_channel.guild.id}).")
                vc = None
            else:
                try:
                    vc = await voice_channel.connect()
                except RuntimeError as e:
                    # Erreur typique si PyNaCl est absent
                    print(f"Erreur en se connectant au vocal : {e}")
                    vc = None
                except Exception as e:
                    print(f"Erreur inattendue lors de la connexion vocale : {e}")
                    vc = None

        # Si la connexion vocale a réussi, jouer le son
        if vc:
            try:
                audio_source = FFmpegOpusAudio(sound_path)
                audio_source = PCMVolumeTransformer(audio_source, volume=0.5)  # volume entre 0.0 et 1.0, 0.5 = 50%
                vc.play(audio_source)

                # Attendre la fin du son
                while vc.is_playing():
                    await asyncio.sleep(1)
            except Exception as e:
                print(f"Impossible de jouer le son: {e}")
            finally:
                try:
                    await vc.disconnect()
                except Exception as e:
                    print(f"Erreur lors de la déconnexion vocale: {e}")
            print(f"Son joué pour {user.name}")
    
    else:
        print(f"L'utilisateur {user.name} n'est pas en vocal, envoi d'un MP...")
        try:
            await user.send("Bouge ton cul. C'est l'heure de la prière.")
        except discord.Forbidden:
            print(f"Impossible d'envoyer un message à {user.name}")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

handle_user_action(bot,"446282191442411520","sounds/notification.mp3")