# 0 */2 * * * /usr/bin/python3 /home/www/b2b/ledure_dev/bridge/JournalEntries/sync_reconcilation.py

import requests, json
import time
import math
import mysql.connector

from datetime import datetime
from datetime import date, datetime, timedelta
import calendar

import sys, os
import urllib.parse

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

currentDate = date.today()
currentDay = calendar.day_name[currentDate.weekday()]  # this will return the day of a week
currentTime = datetime.today().strftime("%I:%M %p")
currentDateTime = f"{currentDate} {currentTime}"
serverDateTime = datetime.now()

print('>>>>>>>>>>>> Ledure Prod <<<<<<<<<<<<<<<<<<<<')
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    # password='root',
    password='F5GB?d4R#SW@r',
    # password='$Bridge@2022#',
    database='ledure_dev',
    # port = '8889',
)
mycursor = mydb.cursor(dictionary=True, buffered=True)

# startDate = date.today() - timedelta(days=10)
startDate = '2023-03-31'
endDate = currentDate

sapUrl = f"http://35.154.67.167:8000//Ledure/General/Reconcilation_New.xsjs?DBName=LEDURE_LIVE_300323&From={startDate}&ToDate={endDate}"
print(sapUrl)
sacAPIRsponse = requests.get(sapUrl, verify=False)
rsponseJson = json.loads(sacAPIRsponse.text)
# print(rsponseJson)
rsponseData = rsponseJson['value']
print("No of Recon", len(rsponseData))
# exit()
allQuery = ""
if len(rsponseData) != 0:
    for obj in rsponseData:
        print(obj['TransId'])
        Line_ID  = obj['Line_ID']
        BPName   = obj['BPName']
        TransId  = obj['TransId']
        # Debit    = obj['Debit']
        # Credit   = obj['Credit']
        ReconSum = obj['ReconSum']

        # docSelectQuery = f"select * from JournalEntries_journalentrylines `JournalEntries_journalentrylines` INNER JOIN JournalEntries_journalentries ON JournalEntries_journalentries.id = JournalEntries_journalentrylines.JournalEntriesId WHERE JournalEntries_journalentries.JdtNum = '{TransId}' LIMIT 1"
        # print(docSelectQuery)
        # mycursor.execute(docSelectQuery)
        # jeData = mycursor.fetchone()
        # if len(jeData) > 0:
        #     reconSum = (float(jeData['Debit']) + float(jeData['Credit'])) - float(jeData['ReconSum'])
        #     print("ReconSum", ReconSum, "reconSum", reconSum)
        #     if reconSum != 0:
        
        updateJE = f"UPDATE `JournalEntries_journalentrylines` INNER JOIN JournalEntries_journalentries ON JournalEntries_journalentries.id = JournalEntries_journalentrylines.JournalEntriesId  SET `ReconSum` = '{ReconSum}' WHERE JournalEntries_journalentries.JdtNum = {TransId} AND JournalEntries_journalentrylines.Line_ID = {Line_ID} AND JournalEntries_journalentrylines.ShortName = '{BPName}';" 
        print(updateJE)
        mycursor.execute(updateJE)
        mydb.commit()
else:
    print(rsponseData)