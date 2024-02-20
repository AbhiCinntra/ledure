# */2 * * * * /usr/bin/python3 /home/www/b2b/vision_sales_support_pre/bridge/Invoice/INV.py
# */2 * * * * /usr/bin/python3 /home/www/b2b/vision_sales_support_dev/bridge/Invoice/INV.py
import requests, json
import time
import math
import mysql.connector

from datetime import datetime
from datetime import date, datetime, timedelta
import calendar

import sys, os
import urllib.parse

currentDate = date.today()
currentDay = calendar.day_name[currentDate.weekday()]  # this will return the day of a week
currentTime = datetime.today().strftime("%I:%M %p")
currentDateTime = f"{currentDate} {currentTime}"
serverDateTime = datetime.now()

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
# mycursor = mydb.cursor(dictionary=True, buffered=True)

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    # password='root',
    password='$Bridge@2022#',
    # password='F5GB?d4R#SW@r',
    database='ledure_pre'
)
mycursor = mydb.cursor(dictionary=True, buffered=True)

print("<><><><><><><><><><><>><><><><><><")
print("===== Login SAP ====")
data = { "CompanyDB": "LEDURE_LIVE_300323", "Password": "L!l@364%$", "UserName": "uneecloud\\led.manager", "SessionId": "7c85460c-c15a-11ed-8000-005056a40bab", "at": "2023-03-13 10:19:30", "sapurl": "https://analytics103u.uneecloud.com:50000/b1s/v1" }
r = requests.post(data['sapurl']+'/Login', data=json.dumps(data), verify=False)
print(r)

lastCode = 0
# mycursor.execute("SELECT * FROM `Company_glaccounts` ORDER BY `id` desc LIMIT 1")
# entryData = mycursor.fetchall()
# if len(entryData) > 0:
#     lastCode = entryData[0]['Code']
#     print(lastCode)

skip=0
# for i in range(count):
while skip != "":
    # sapAPIUrl = f"/ChartOfAccounts?$filter = Code gt {lastCode}&$skip = {skip}"
    sapAPIUrl = f"/ChartOfAccounts?$skip = {skip}"
    print(sapAPIUrl)
    res = requests.get(data['sapurl']+sapAPIUrl, cookies=r.cookies, verify=False)
    # print(res.text)
    opts = json.loads(res.text)
    print("no of Accounts",len(opts['value']))
    for opt in opts['value']:
        # print(opt)
        Code = opt['Code']
        Name = opt['Name'].replace("'","").replace('"', '')
        print("Code: ", Code)

        checkPaymentQuery = f"select * from Company_glaccounts WHERE Code = '{Code}'"
        print(checkPaymentQuery)
        mycursor.execute(checkPaymentQuery)
        if mycursor.rowcount == 0:
            add_sql = f'INSERT INTO `Company_glaccounts`(`Code`, `Name`) VALUES("{Code}", "{Name}")'
            print(add_sql) 
            mycursor.execute(add_sql)
            mydb.commit()

        # endif
    # endfor
    if 'odata.nextLink' in opts:
        nextLink = opts['odata.nextLink']
        print(">>>>>>>>>>>>>>>>>>>>> nextLink: ", nextLink)
        nextLink = nextLink.split("skip=")
        print(nextLink)
        skip = str(nextLink[1]).strip()
    else:
        print("<<<<<<<<<<<<<<<<<<<<< nextLink: ", "")
        skip = ""
        exit()
    print("skip", skip)
# endWhile