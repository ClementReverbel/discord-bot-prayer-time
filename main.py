import discord
import logging
from discord.ext import commands
from dotenv import load_dotenv
import os
import json
# Preparation
import pycurl
import certifi
from io import BytesIO

# Set buffer and Curl object.
buffer = BytesIO()
c = pycurl.Curl()

# Set request options.
## Set the request destination.
URl_BASE = 'https://api.aladhan.com/v1/timingsByAddress/'
date = '11-11-2025'
ville = 'Neuchatel'
decalage_min = '20'
URL = URl_BASE + date + '?address=' + ville
c.setopt(c.URL, URL)

## Set the buffer as the destination of the request's response.
c.setopt(c.WRITEDATA, buffer)

## Refer to the installed certificate authority bundle for validating the SSL certificate.
c.setopt(c.CAINFO, certifi.where())

# Execute and close the request.
c.perform()
c.close()

# Print the buffer's content with a Latin1 (iso-8859-1) encoding.
body = buffer.getvalue()
data = body.decode('iso-8859-1')

data = json.loads(data)

# Fonction pour retirer le décalage aux temps de prière
def ajust_time(time_str, decalage_min):

    from datetime import datetime, timedelta
    
    # Convertir decalage_min en entier
    decalage = int(decalage_min)
    
    # Parser l'heure (format hh:mm)
    time_obj = datetime.strptime(time_str, '%H:%M')
    
    # Soustraire le décalage
    adjusted_time = time_obj - timedelta(minutes=decalage)
    
    # Retourner au format hh:mm
    return adjusted_time.strftime('%H:%M')

fajr = data["data"]["timings"]["Fajr"]
Dhuhr = data["data"]["timings"]["Dhuhr"]
Asr = data["data"]["timings"]["Asr"]
Maghrib = data["data"]["timings"]["Maghrib"]
Isha = data["data"]["timings"]["Isha"]

fajr_alarm = ajust_time(fajr, decalage_min)
Dhuhr_alarm = ajust_time(Dhuhr, decalage_min)
Asr_alarm = ajust_time(Asr, decalage_min)
Maghrib_alarm = ajust_time(Maghrib, decalage_min)
Isha_alarm = ajust_time(Isha, decalage_min)


