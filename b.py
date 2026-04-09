"""
For some reason w+ yields no permission errors, while w does

TODO: Write multiple data handlers w/ command line options
TODO: Send visuals along with data pairs
TODO: Experiment with alternative email servers (other than gmail)

Fetching custom ebird API request and sending it via email

You need to write a file (.env) in the same directory with the following variables:

DEFAULT:    the default gmail to send results to if no -r option is given
EMAIL:      the gmail you are using to send data
EMAILPASS:  a password to the gmail you are using to send data
TOKEN:      a valid eBird token for use with the API

To do this in Windows reliably, use the following commands in terminal

cd ./path/to/your/project
touch .env
notepad .env  (or whatever editor you use)

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

load_dotenv()

if os.getenv('TOKEN') == '':
    raise Exception(f'No token, no bueno')

parser = argparse.ArgumentParser(description="""
Send custom eBird alerts to an email you designate\n
You need to write a file (.env) in the same directory with the following variables:\n
DEFAULT:    the default gmail to send results to if no -r option is given\n
EMAIL:      the gmail you are using to send data\n
EMAILPASS:  a password to the gmail you are using to send data\n
TOKEN:      a valid eBird token for use with the API\n
e.g. python b.py -r youremail@domain.com\n\n
""", formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument(
    '-r',
    nargs='?',
    default= os.getenv('DEFAULT'),
    help='the recipient email you want the alert sent to\n defaults to the email set in your .env file')#string type assumed as default
args = parser.parse_args()


#function that requests ebird API and returns a string of desired obs data to be send over email
#Need handlers for different types of calls / alerts
def getNearby():

        #Getting the data
        url = 'https://api.ebird.org/v2/data/obs/geo/recent?lat=35.2916363&lng=-80.7269854&includeProvisional=true&back=1&maxResults=50'
        headers = {'x-ebirdapitoken': os.getenv('TOKEN')}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise ValueError(f'The response status was {response.status_code}')
            return "Handled Error"
        data = response.json()
        #saving data to file
        with open('C:/Users/jackg/Desktop/b/alertData.txt', 'w+') as file:
                json.dump(data, file)

        #transforming the data from an array of dictionaries to string of meaningful info
        index = [elem['obsDt'] for elem in data] # list of strings
        columns = [species['comName']for species in data]
        test = pd.Series(index=index, data=columns)
        counts = test.value_counts() # shows counts per species
        v = pd.DataFrame(data=counts, index=test.array) #test.array shows the keys as a list
        body = v.to_string() #to_html seems to send the text of html version
        body = v.to_html()
        return body

#sends data by email to designated recipient from env set gmail
def sendData(RECIPIENT, body):

    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    EMAIL_ADDR = os.getenv('EMAIL')
    EMAIL_PASS = os.getenv('EMAILPASS')

    message = EmailMessage()
    message.add_header('From', EMAIL_ADDR)
    message.add_header('To', RECIPIENT)
    message.add_header('Subject','Bird Sightings')
    message.add_header('Content-Type', 'text/html; charset="utf-8"')
    message.set_content(body, subtype='html')

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as mailserver:
            mailserver.starttls()
            mailserver.login(EMAIL_ADDR, EMAIL_PASS)
            #mailserver.sendmail(EMAIL_ADDR, RECIPIENT, message)
            mailserver.sendmail(EMAIL_ADDR, RECIPIENT, message.as_string())
            print('finished')
            return 1
    except smtplib.SMTPException as e:
        print(e)
        return


#prevents code execution if imported
if __name__=='__main__':
    data = getNearby()
    sendData(args.r, data)
