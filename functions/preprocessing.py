from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime, timedelta
from time import strftime
import bd.acces_bd as bd
import functions.callAPI as API

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

def prayer_adjust_time(date=strftime("%d-%m-%Y"),ville="Neuchatel",decalage_min="20"):
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
    for prayer_time in prayer_list:
        alarm_list.append(ajust_time(prayer_time, decalage_min))
    
    return alarm_list

def set_reminder_by_user(user,ville,decalage):
    bd.delete_time(user)
    horaires=prayer_adjust_time(ville=ville,decalage_min=decalage)
    for h in horaires:
        bd.insert_time(h,user)

