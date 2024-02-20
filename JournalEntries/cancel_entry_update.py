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
    database='ledure_dev',
    # port = '8889',
)
mycursor = mydb.cursor(dictionary=True, buffered=True)

# startDate = date.today() - timedelta(days=10)
startDate = '2023-03-31'
endDate = currentDate

# sapUrl = f"http://35.154.67.167:8000//Ledure/General/Reconcilation_New.xsjs?DBName=LEDURE_LIVE_300323&From={startDate}&ToDate={endDate}"
sapUrl = f"http://35.154.67.167:8000/Ledure/Report/CancelTransaction.xsjs"
print(sapUrl)
sacAPIRsponse = requests.get(sapUrl, verify=False)
rsponseJson = json.loads(sacAPIRsponse.text)
# print(rsponseJson)
rsponseData = rsponseJson['CancelDocument']["0"]
print("No of CancelEntry", len(rsponseData))
# exit()
allQuery = ""
if len(rsponseData) != 0:
    for obj in rsponseData:
        print(obj['TransId'])
        TransId     = obj['TransId']
        # Document    = obj['Document Type']
        ObjType     = obj['ObjType']
        DocNum      = obj['DocNum']
        DocumentDate = obj['DocumentDate']
        DocTotal    = obj['DocTotal']
        U_Cancel    = obj['U_Cancel']
        U_InterTransaction = obj['U_InterTransaction']

        # update cancel status of Journal Entries
        updateJE = f"UPDATE `JournalEntries_journalentries` SET `U_Cancel` = '{U_Cancel}', `U_InterTransaction` = '{U_InterTransaction}' WHERE `JdtNum` = '{TransId}';" 
        print(updateJE)
        mycursor.execute(updateJE)
        mydb.commit()

        # continue

        # update cancel status of Invoice
        if ObjType == "13":
            updateInv = f"UPDATE `Invoice_invoice` SET `CancelStatus` = 'csYes' WHERE DocNum = '{DocNum}';" 
            print(updateInv)
            mycursor.execute(updateInv)
            mydb.commit()

        # update cancel status of credite note
        elif ObjType == "14":
            updateInv = f"UPDATE `Invoice_creditnotes` SET `CancelStatus` = 'csYes' WHERE DocNum = '{DocNum}';" 
            print(updateInv)
            mycursor.execute(updateInv)
            mydb.commit()

        # update cancel status of Purchase Invoice
        elif ObjType == "18":
            updateInv = f"UPDATE `PurchaseInvoices_purchaseinvoices` SET `CancelStatus` = 'csYes' WHERE DocNum = '{DocNum}';"
            print(updateInv)
            mycursor.execute(updateInv)
            mydb.commit()

        # update cancel status of Purchase CreditNOte
        elif ObjType == "19":
            updateInv = f"UPDATE `PurchaseInvoices_purchasecreditnotes` SET `CancelStatus` = 'csYes' WHERE DocNum = '{DocNum}';"
            print(updateInv)
            mycursor.execute(updateInv)
            mydb.commit()

        # update cancel status of Incomming Payments
        elif ObjType == "24":
            updateInv = f"UPDATE `Invoice_incomingpayments` SET `JournalRemarks` = 'Canceled' WHERE DocNum = '{DocNum}';"
            print(updateInv)
            mycursor.execute(updateInv)
            mydb.commit()
        # end else
    # end for
# end if
else:
    print(rsponseData)