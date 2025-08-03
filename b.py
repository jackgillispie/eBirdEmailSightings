"""
TODO: Write multiple data handlers w/ command line options
TODO: Add help flags

Fetching customer ebird API request and sending it to my email

You need to write a file (.env.txt) in the same directory with the following variables:

DEFAULT:    the default gmail to send results to if no -r option is given
EMAIL:      the gmail you are using to send data
EMAILPASS:  a password to the gmail you are using to send data
TOKEN:      a valid eBird token for use with the API

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
import argparse


c = dotenv_values(".env.txt")#use the full file name, not just .env ; Windows having issues w/ naming the file 

parser = argparse.ArgumentParser(description='set recipient email')
parser.add_argument(
    '-r',
    nargs='?',
    default=c['DEFAULT'],
    help='type the email you want the alert sent to')#string type assumed as default
args = parser.parse_args()
print(args.r)

#function that requests ebird API and returns a string of desired obs data to be send over email
#Need to make many handlers for different types of calls / alerts
def getNearby():
    
    #Getting the data
    url = 'https://api.ebird.org/v2/data/obs/geo/recent?lat=35.2916363&lng=-80.7269854&includeProvisional=true&back=1&maxResults=20'
    headers = {'x-ebirdapitoken': c['TOKEN']}
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)#array of dictionaries, one for each obs

    #transforming the data
    index = [elem['obsDt'] for elem in data]
    columns = [species['comName']for species in data]
    test = pd.Series(index=index, data=columns)
    counts = test.value_counts() # shows counts per species
    v = pd.DataFrame(data=counts, index=test.array) #test.array shows the keys as a list
    body = v.to_string() #to_html seems to send the text of html version
    
    return body


#sends data by email to designated recipient from env set gmail  
def sendData(RECIPIENT, body):
        
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    EMAIL_ADDR = c['EMAIL']
    EMAIL_PASS = c['EMAILPASS']

    message = EmailMessage()
    message.add_header('From', EMAIL_ADDR)
    message.add_header('To', RECIPIENT)
    message.add_header('Subject','Bird Sightings')
    message.set_content(body)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as mailserver:
        mailserver.starttls()
        mailserver.login(EMAIL_ADDR, EMAIL_PASS)
        mailserver.sendmail(EMAIL_ADDR, RECIPIENT, message.as_string())
        
    print('finished')



#prevents code execution if imported
if __name__=='__main__':
    data = getNearby()
    sendData(args.r, data)






