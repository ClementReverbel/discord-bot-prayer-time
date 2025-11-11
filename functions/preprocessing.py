from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime, timedelta
from time import strftime, sleep
import bd.acces_bd as bd
import functions.callAPI as API
import asyncio
import functions.core as core

def prayer_time(date=strftime("%d-%m-%Y"), ville="Neuchatel"):

    data = API.getRawDataPrayerTime(date, ville)
    fajr = data["data"]["timings"]["Fajr"]
    Dhuhr = data["data"]["timings"]["Dhuhr"]
    Asr = data["data"]["timings"]["Asr"]
    Maghrib = data["data"]["timings"]["Maghrib"]
    Isha = data["data"]["timings"]["Isha"]
    
    prayer_list = []
    prayer_list.append(fajr)
    prayer_list.append(Dhuhr)
    prayer_list.append(Asr)
    prayer_list.append(Maghrib)
    prayer_list.append(Isha)
    
    return prayer_list

def prayer_adjust_time(ville,decalage_min,date=strftime("%d-%m-%Y")):
    # Fonction pour retirer le décalage aux temps de prière
    def ajust_time(time_str, decalage):
            
        # Convertir decalage_min en entier
        decalage = int(decalage)
        
        # Parser l'heure (format hh:mm)
        time_obj = datetime.strptime(time_str, '%H:%M')
        
        # Soustraire le décalage
        adjusted_time = time_obj - timedelta(minutes=decalage)
        
        # Retourner au format hh:mm
        return adjusted_time.strftime('%H:%M')

    prayer_list=prayer_time(date, ville)
    
    alarm_list=[]
    for time in prayer_list:
        alarm_list.append(ajust_time(time, decalage_min))
    
    return alarm_list

def set_reminder_by_user(user,ville,decalage):
    bd.delete_time(user)
    horaires=prayer_adjust_time(ville=ville,decalage_min=decalage)
    for h in horaires:
        bd.insert_time(h,user)

def get_all_times_set():
    rows = bd.get_all_time()
    return {r[0] for r in rows} if rows else set()

async def watch_times_forever(bot):
    while True:
        now = datetime.now()
        current_time = now.strftime('%H:%M')
        times = get_all_times_set()
        if current_time in times:
            users = bd.get_users_by_time(current_time)
            users = [u[0] for u in users]
            for user_id in users:
                await core.handle_user_action(bot, user_id, "./sounds/notification.mp3")

        # Dormir jusqu'à la prochaine minute (précis au niveau des secondes)
        seconds_to_next_minute = 60 - now.second - now.microsecond / 1_000_000
        await asyncio.sleep(seconds_to_next_minute)