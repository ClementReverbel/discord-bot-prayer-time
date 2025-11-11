from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime, timedelta
from time import strftime
import functions.callAPI as API


def prayer_adjust_time(date=strftime("%d-%m-%Y"),ville="Neuchatel"):

    # Fonction pour retirer le décalage aux temps de prière
    def ajust_time(time_str, decalage_min="20"):
            
        # Convertir decalage_min en entier
        decalage = int(decalage_min)
        
        # Parser l'heure (format hh:mm)
        time_obj = datetime.strptime(time_str, '%H:%M')
        
        # Soustraire le décalage
        adjusted_time = time_obj - timedelta(minutes=decalage)
        
        # Retourner au format hh:mm
        return adjusted_time.strftime('%H:%M')

    prayer_list=prayer_time(date, ville)
    
    alarm_list=[]
    for prayer_time in prayer_list:
        alarm_list.append(ajust_time(prayer_time))
    
    return alarm_list


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


