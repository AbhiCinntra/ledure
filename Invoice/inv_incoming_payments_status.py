import requests, json
import time
import math
import mysql.connector

from datetime import datetime
from datetime import date, datetime, timedelta
import calendar

import sys, os

currentDate = date.today()
currentDay = calendar.day_name[currentDate.weekday()]  # this will return the day of a week
currentTime = datetime.today().strftime("%I:%M %p")
currentDateTime = f"{currentDate} {currentTime}"
serverDateTime = datetime.now()

# print('>>>>>>>>>>>> shivtara_live <<<<<<<<<<<<<<<<<<<<')
# import sys, os
# dir = os.getcwd()
# dir = dir.split("bridge")[0]+"bridge"
# sys.path.append(dir)
# from bridge import settings
# data = settings.SAPSESSION("core")

# mydb = mysql.connector.connect(
#   host=settings.DATABASES['default']['HOST'],
#   user=settings.DATABASES['default']['USER'],
#   password=settings.DATABASES['default']['PASSWORD'],
#   database=settings.DATABASES['default']['NAME']
# )
# mycursor = mydb.cursor()


mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    # password='root',
    # password='$Bridge@2022#',
    password='F5GB?d4R#SW@r',
    database='ledure_dev'
)
mycursor = mydb.cursor(buffered=True)

print("<><><><><><><><><><><>><><><><><><")
print("===== Login SAP ====")
data = {"CompanyDB": "LEDURE_LIVE_300323", "Password": "1020", "UserName": "PRO001", "SessionId": "d802ea02-512e-11ee-8000-0a427ed74412", "at": "2023-09-12 11:10:12", "sapurl": "https://35.154.67.167:50000/b1s/v1"}
r = requests.post(data['sapurl']+'/Login', data=json.dumps(data), verify=False)
# print(r)
currentDate = date.today() - timedelta(days=10)
invCount = requests.get(data["sapurl"]+"/IncomingPayments/$count", cookies=r.cookies, verify=False).text

# count the number if loop run, each one skip 20 values
count = math.ceil(int(invCount)/20)
# print(count)
if int(count) > 0:
    skip=0
    for i in range(count):
        baseUrl = data["sapurl"]+"/IncomingPayments?$orderby = DocEntry asc&$select=DocEntry,DocNum,DocType,CardCode,CardName,JournalRemarks&$skip="+str(skip)
        print(baseUrl)
        res = requests.get(baseUrl, cookies=r.cookies, verify=False)
        opts = json.loads(res.text)
        # print(opts)
        for opt in opts['value']:
            DocEntry = opt['DocEntry']
            print("DocEntry: ", DocEntry)
            docSelectQuery = f"select * from Invoice_incomingpayments WHERE DocEntry = '{DocEntry}'"
            print(docSelectQuery)
            mycursor.execute(docSelectQuery)
            mycursor.fetchall()
            if mycursor.rowcount > 0:                
                CardCode = opt['CardCode']
                JournalRemarks = opt['JournalRemarks']
                ord_sql = f"UPDATE `Invoice_incomingpayments` SET `JournalRemarks`='{JournalRemarks}' WHERE DocEntry = '{DocEntry}'"
                print(ord_sql)
                mycursor.execute(ord_sql)
                mydb.commit()             
                # InvoiceID = mycursor.lastrowid

        print('___')
        skip = skip+20
        print(skip)