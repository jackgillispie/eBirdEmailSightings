"""

Fetching customer ebird API request and sending it to my email

TODO: Reformat for command line use / OOP style

NOTE: Windows is being finnicky with load_dotenv() despite changing encoding
of file
"""



import requests
import os
from dotenv import load_dotenv, dotenv_values
import json
import pandas as pd

import matplotlib.pyplot as plt
import smtplib
from email.mime.text import MIMEText
from email.message import EmailMessage

from email.mime.multipart import MIMEMultipart


c = dotenv_values(".env.txt")#use the full file name, not just .env

print(c['EMAIL'])
url = 'https://api.ebird.org/v2/data/obs/geo/recent?lat=35.2916363&lng=-80.7269854&includeProvisional=true&back=1&maxResults=5'
headers = {'x-ebirdapitoken': c['TOKEN']}
response = requests.get(url, headers=headers)
data = json.loads(response.text)#array of dictionaries, one for each obs
index = [ elem['obsDt'] for elem in data]
columns = [species['comName']for species in data]
test = pd.Series(index=index, data=columns)
#test.array shows the keys as a list
counts = test.value_counts() # shows counts per species
v = pd.DataFrame(data=counts, index=test.array)



body = v.to_string() #to_html seems to send the text of html version

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDR = c['EMAIL']
EMAIL_PASS = c['EMAILPASS']

message = EmailMessage()
message.add_header('From', EMAIL_ADDR)
message.add_header('To', 'jack.gillispie15@gmail.com')
message.add_header('Subject','Bird Sightings')
message.set_content(body)

with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as mailserver:
    mailserver.starttls()
    mailserver.login(EMAIL_ADDR, EMAIL_PASS)
    mailserver.sendmail(EMAIL_ADDR, 'jack.gillispie15@gmail.com', message.as_string())








