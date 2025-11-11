from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime, timedelta
import callAPI as API


def prayer_adjust_time(date=None,ville=None):

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

    data = API.getRawDataPrayerTime(date,ville)
    fajr = data["data"]["timings"]["Fajr"]
    Dhuhr = data["data"]["timings"]["Dhuhr"]
    Asr = data["data"]["timings"]["Asr"]
    Maghrib = data["data"]["timings"]["Maghrib"]
    Isha = data["data"]["timings"]["Isha"]
    
    alarm_list=[]
    alarm_list.append(ajust_time(fajr))
    alarm_list.append(ajust_time(Dhuhr))
    alarm_list.append(ajust_time(Asr))
    alarm_list.append(ajust_time(Maghrib))
    alarm_list.append(ajust_time(Isha))
    
    return alarm_list


