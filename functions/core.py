import discord
import asyncio

async def handle_user_action(bot: discord.Client, user_id: int, sound_path: str):
    user = await bot.fetch_user(user_id)
    guilds = bot.guilds  # liste des serveurs où le bot est présent

    voice_channel = None

    for guild in guilds:
        member = guild.get_member(user_id)
        if member and member.voice and member.voice.channel:
            voice_channel = member.voice.channel
            break

    if voice_channel:
        print(f"L'utilisateur {user.name} est dans le salon {voice_channel.name}")
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
