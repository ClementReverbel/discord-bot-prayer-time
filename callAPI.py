import json
import pycurl
import certifi
from time import strftime
from io import BytesIO

def getRawDataPrayerTime(date=strftime("%d-%m-%Y"),ville="Neuchatel"):
    # Set buffer and Curl object.
    buffer = BytesIO()
    c = pycurl.Curl()

    # Set request options.
    ## Set the request destination.
    URl_BASE = 'https://api.aladhan.com/v1/timingsByAddress/'
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
    return json.loads(data)



print(getRawDataPrayerTime())