# */2 * * * * /usr/bin/python3 /home/www/b2b/shivtara_live/bridge/Invoice/INV.py
# */2 * * * * /usr/bin/python3 /home/www/b2b/shivtara_live/bridge/Invoice/INV.py
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

print('>>>>>>>>>>>> shivtara_live <<<<<<<<<<<<<<<<<<<<')
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
    password='F5GB?d4R#SW@r',
    # password='$Bridge@2022#',
    database='ledure_dev'
)
mycursor = mydb.cursor(dictionary=True, buffered=True)

print("<><><><><><><><><><><>><><><><><><")
print("===== Login SAP ====")
data = {"CompanyDB": "LEDURE_LIVE_300323", "Password": "1020", "UserName": "PRO001", "SessionId": "d802ea02-512e-11ee-8000-0a427ed74412", "at": "2023-09-12 11:10:12", "sapurl": "https://35.154.67.167:50000/b1s/v1"}
r = requests.post(data['sapurl']+'/Login', data=json.dumps(data), verify=False)
print(r)

# currentDate = '2023-03-13'
# currentDate = date.today() - timedelta(days=10)
# # count = requests.get(data['sapurl']+'/DeliveryNotes/$count?$filter=UpdateDate ge '+str(currentDate)+'', headers={'Authorization': "Bearer "+data['SessionId']+""}, verify=False).text
# invCount = requests.get(data['sapurl']+'/DeliveryNotes/$count?$filter=UpdateDate ge '+str(currentDate), cookies=r.cookies, verify=False).text

# # count the number if loop run, each one skip 20 values
# count = math.ceil(int(invCount)/20)
# print(count)

lastDocEntry = 0
mycursor.execute("SELECT * FROM `DeliveryNote_deliverynote` ORDER BY `id` desc LIMIT 1")
entryData = mycursor.fetchall()
if len(entryData) > 0:
    lastDocEntry = entryData[0]['DocEntry']
    print(lastDocEntry)

if True:
    skip=0
    while skip != "": 

        # res = requests.get(data['sapurl']+'/DeliveryNotes?$filter=UpdateDate ge '+str(currentDate)+'&$skip='+str(skip)+'', cookies=r.cookies, verify=False)
        sapAPIUrl = f"/DeliveryNotes?$filter = DocEntry gt {lastDocEntry}&$skip = {skip}"
        print(sapAPIUrl)
        res = requests.get(data['sapurl']+sapAPIUrl, cookies=r.cookies, verify=False)
        # print(res.text)
        opts = json.loads(res.text)
        for opt in opts['value']:
            DocEntry = opt['DocEntry']
            print("DocEntry: ", DocEntry)
            # OrderID = str(opt['U_PORTAL_NO']) # local order id
        
            docSelectQuery = f"select * from DeliveryNote_deliverynote WHERE DocEntry = '{DocEntry}'"
            print(docSelectQuery)
            mycursor.execute(docSelectQuery)
            mycursor.fetchall()
            if mycursor.rowcount != 1:

                BaseType = opt['DocumentLines'][0]['BaseType']
                # if str(BaseType) != 17 or str(BaseType) != 15:
                if str(BaseType) != '17':
                    print("<><><><><><><><><", str(BaseType))
                    continue
                else:
                    print(">>>>>>>>>>>>>>>>>", str(BaseType))
                        
                d = datetime.strptime(str(opt['DocTime']), "%H:%M:%S")
                DocTime = d.strftime("%I:%M:%S %p")

                e = datetime.strptime(str(opt['UpdateTime']), "%H:%M:%S")
                UpdateTime = e.strftime("%I:%M:%S %p")  

                discountPercent = str(opt['DiscountPercent'])
                if discountPercent == "None":
                    discountPercent = 0
    
                CardCode = opt['CardCode']
                
                # str(discountPercent)
                DocTotal = opt['DocTotal']
                CardName = str(opt['CardName']).replace("'","\\'")
                ord_sql = "INSERT INTO `DeliveryNote_deliverynote`(`TaxDate`, `DocDueDate`, `ContactPersonCode`, `DiscountPercent`, `DocDate`, `CardCode`, `Comments`, `SalesPersonCode`, `DocumentStatus`, `DocCurrency`, `DocTotal`, `CardName`, `VatSum`, `CreationDate`, `DocEntry`, `CreateDate`, `CreateTime`, `UpdateDate`, `UpdateTime`, `OrderID` ,`CancelStatus`) VALUES ('"+str(opt['TaxDate'])+"', '"+str(opt['DocDueDate'])+"', '"+str(opt['ContactPersonCode'])+"', '"+str(discountPercent)+"', '"+str(opt['DocDate'])+"', '"+str(opt['CardCode'])+"', '"+str(opt['Comments'])+"', '"+str(opt['SalesPersonCode'])+"', '"+str(opt['DocumentStatus'])+"', '"+str(opt['DocCurrency'])+"', '"+str(opt['DocTotal'])+"', '"+str(CardName)+"', '"+str(opt['VatSum'])+"', '"+str(opt['CreationDate'])+"', '"+str(opt['DocEntry'])+"', '"+str(opt['CreationDate'])+"','','', '"+str(UpdateTime)+"', '', '"+str(opt['CancelStatus'])+"')"
            
                print(ord_sql)
                mycursor.execute(ord_sql)
                mydb.commit()                
                DeliveryNoteID = mycursor.lastrowid
                
                add = opt['AddressExtension']

                U_SCOUNTRY  = ""
                U_SSTATE    = ""
                U_SHPTYPB   = ""
                U_BSTATE    = ""
                U_BCOUNTRY  = ""
                U_SHPTYPS   = ""

                ShipToBuilding = str(add['ShipToBuilding']).replace("'","\\'")
                BillToBuilding = str(add['BillToBuilding']).replace("'","\\'")
                ShipToStreet = str(add['ShipToStreet']).replace("'","\\'")
                BillToStreet = str(add['BillToStreet']).replace("'","\\'")

                add_sql = "INSERT INTO `DeliveryNote_addressextension`(`DeliveryNoteID`, `BillToBuilding`, `ShipToState`, `BillToCity`, `ShipToCountry`, `BillToZipCode`, `ShipToStreet`, `BillToState`, `ShipToZipCode`, `BillToStreet`, `ShipToBuilding`, `ShipToCity`, `BillToCountry`, `U_SCOUNTRY`, `U_SSTATE`, `U_SHPTYPB`, `U_BSTATE`, `U_BCOUNTRY`, `U_SHPTYPS`) VALUES ('"+str(DeliveryNoteID)+"', '"+str(BillToBuilding)+"', '"+str(add['ShipToState'])+"', '"+str(add['BillToCity'])+"', '"+str(add['ShipToCountry'])+"', '"+str(add['BillToZipCode'])+"', '"+str(ShipToStreet)+"', '"+str(add['BillToState'])+"', '"+str(add['ShipToZipCode'])+"', '"+str(BillToStreet)+"', '"+str(ShipToBuilding)+"', '"+str(add['ShipToCity'])+"', '"+str(add['BillToCountry'])+"', '"+str(U_SCOUNTRY)+"', '"+str(U_SSTATE)+"', '"+str(U_SHPTYPB)+"', '"+str(U_BSTATE)+"', '"+str(U_BCOUNTRY)+"', '"+str(U_SHPTYPS)+"');"
                print(add_sql)                
                mycursor.execute(add_sql)
                mydb.commit()

                itemCount = 0
                totalPrice = DocTotal
                for line in opt['DocumentLines']:
                    print(line['Quantity'])
                    print(line['DiscountPercent'])
                    
                    # if line['DiscountPercent'] == None or line['DiscountPercent'] == 0:
                    #     lDiscountPercent = 0.0
                    # else:
                    #     lDiscountPercent = float(line['DiscountPercent'])
                    # str(lDiscountPercent)

                    lDiscountPercent = str(line['DiscountPercent'])
                    if lDiscountPercent == "None":
                        lDiscountPercent = 0


                    BaseEntry = str(line['BaseEntry']) # sap order id
                    TaxRate = str(line['TaxPercentagePerRow'])

                    FreeText = str(line['FreeText']).replace("'","\\'")
                    line_sql = "INSERT INTO `DeliveryNote_documentlines`(`LineNum`, `DeliveryNoteID`, `Quantity`, `UnitPrice`, `DiscountPercent`, `ItemDescription`, `ItemCode`, `TaxCode`, `BaseEntry`, `TaxRate`, `UomNo`) VALUES ('"+str(line['LineNum'])+"', '"+str(DeliveryNoteID)+"', '"+str(line['Quantity'])+"', '"+str(line['UnitPrice'])+"', '"+str(lDiscountPercent)+"', '"+str(line['ItemDescription'])+"', '"+str(line['ItemCode'])+"', '"+str(line['TaxCode'])+"', '"+str(BaseEntry)+"', '"+str(TaxRate)+"', '"+str(line['UoMCode'])+"');"

                    # totalPrice = float(float(totalPrice) + float(line['UnitPrice']))

                    print(line_sql)
                    mycursor.execute(line_sql)
                    mydb.commit()
                    itemCount = itemCount+1
         

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
    # endwhile
# endIf


