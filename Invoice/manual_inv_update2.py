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
import urllib.parse

currentDate = date.today()
currentDay = calendar.day_name[currentDate.weekday()]  # this will return the day of a week
currentTime = datetime.today().strftime("%I:%M %p")
currentDateTime = f"{currentDate} {currentTime}"
serverDateTime = datetime.now()

#print('>>>>>>>>>>>> shivtara_live <<<<<<<<<<<<<<<<<<<<')
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
    # database='ledure_pre'
    password='F5GB?d4R#SW@r',
    database='ledure_dev'
)
mycursor = mydb.cursor(dictionary=True, buffered=True)

#print("<><><><><><><><><><><>><><><><><><")
#print("===== Login SAP ====")
data = {"CompanyDB": "LEDURE_LIVE_300323", "Password": "1020", "UserName": "PRO001", "SessionId": "71b3e58c-52ee-11ee-8000-0a427ed74412", "at": "2023-09-14 22:00:55", "sapurl": "https://35.154.67.167:50000/b1s/v1"}
r = requests.post(data['sapurl']+'/Login', data=json.dumps(data), verify=False)
#print(r)


lastDocEntry = 0
# mycursor.execute("SELECT * FROM `Invoice_invoice` ORDER BY `id` desc LIMIT 1")
mycursor.execute("SELECT * FROM `Invoice_invoice` WHERE DocumentStatus = 'bost_open' AND CancelStatus = 'csNo'")
entryData = mycursor.fetchall()
# if len(entryData) > 0:
for entry in entryData:
    lastDocEntry = entry['DocEntry']
    print(lastDocEntry)

    # sapAPIUrl = f"/Invoices?$filter = DocEntry ge {lastDocEntry}&$select=DocEntry,DocNum,CardCode,WTAmount,U_E_INV_NO,U_E_INV_Date,U_TransporterID,U_TransporterName,U_VehicalNo,U_UNE_LRNo,U_UNE_LRDate,OriginalRefNo,OriginalRefDate,PaidToDateSys,DocumentStatus,CancelStatus,GSTTransactionType,DiscountPercent&$skip = {skip}&$orderby=DocEntry"
    sapAPIUrl = f"/Invoices?$filter = DocEntry eq {lastDocEntry}"
    print(sapAPIUrl)
    res = requests.get(data['sapurl']+sapAPIUrl, cookies=r.cookies, headers={"Prefer":"odata.maxpagesize=100"}, verify=False)
    opts = json.loads(res.text)
    # #print(res.text)
    for opt in opts['value']:

        DocNum = opt['DocNum']
        DocEntry = opt['DocEntry']
        print("Top DocEntry: ", DocEntry)
        # OrderID = str(opt['U_PORTAL_NO']) # local order id
    
        docSelectQuery = f"select * from Invoice_invoice WHERE DocEntry = '{DocEntry}'"
        # print(docSelectQuery)
        mycursor.execute(docSelectQuery)
        invData = mycursor.fetchall()
        # print("rcount: ", mycursor.rowcount)
        if mycursor.rowcount == 1:
            
            InvoiceID = invData[0]['id']
            d = datetime.strptime(str(opt['DocTime']), "%H:%M:%S")
            DocTime = d.strftime("%I:%M:%S %p")

            e = datetime.strptime(str(opt['UpdateTime']), "%H:%M:%S")
            UpdateTime = e.strftime("%I:%M:%S %p")  

            discountPercent = opt['DiscountPercent']
            # print("discountPercent Befour", discountPercent)
            if str(discountPercent) == 'None':
                discountPercent = 0.0
            # print("discountPercent after", discountPercent)

            CardCode = opt['CardCode']
            DeliveryCharge = 0
            AdditionalCharges = 0
            if len(opt['DocumentAdditionalExpenses']) !=0:
                for val in opt['DocumentAdditionalExpenses']:
                    AdditionalCharges = AdditionalCharges + float(val['LineTotal'])

            DocTotal        = opt['DocTotal']
            CardName        = str(opt['CardName']).replace("'","").replace("\\", "")
            Comments        = str(opt['Comments']).replace("'","").replace("\\", "")
            BPLID           = str(opt['BPL_IDAssignedToInvoice'])
            BPLName         = str(opt['BPLName'])
            WTAmount        = str(opt['WTAmount'])
            U_E_INV_NO      = str(opt['U_E_INV_NO'])
            U_E_INV_Date    = str(opt['U_E_INV_Date'])
            U_TransporterID = str(opt['U_TransporterID'])
            U_TransporterName = str(opt['U_TransporterName'])
            U_VehicalNo     = str(opt['U_VehicalNo'])
            NumAtCard       = str(opt['NumAtCard']).replace("'","").replace("\\", "")
            U_UNE_LRNo      = str(opt['U_UNE_LRNo'])
            U_UNE_LRDate    = str(opt['U_UNE_LRDate'])
            U_UNE_IRN       = str(opt['U_UNE_IRN'])
            OriginalRefNo   = str(opt['OriginalRefNo'])
            OriginalRefDate = str(opt['OriginalRefDate'])
            GSTTransactionType  = str(opt['GSTTransactionType'])
            PaidToDateSys   = str(opt['PaidToDateSys'])
            GSTRate         = 0.0
            IRNNo           = ""
            CNNo            = ""
            Address         = str(opt['Address']).replace("'","").replace('"', "")
            Address2        = str(opt['Address2']).replace("'","").replace('"', "")
            VATRegNum       = str(opt['VATRegNum']).replace("'","").replace("\\", "")
            DocNum          = str(opt['DocNum'])

            IGST = 0.0
            CGST = 0.0
            SGST = 0.0
            GSTRate = 0.0

            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            seriesNameURL = f"http://35.154.67.167:8000//Ledure/General/SeriesName.xsjs?DBName=LEDURE_LIVE_300323&DocEntry={DocEntry}&ObjType=13"
            print(seriesNameURL)
            seriesNameResponse = requests.get(seriesNameURL, cookies=r.cookies, verify=False)
            seriesNameJson = json.loads(seriesNameResponse.text)
            seriesNameData = seriesNameJson['value']
            if len(seriesNameData) > 0:
                IRNNo   = seriesNameData[0]['IRNNo']
                CNNo    = f"{seriesNameData[0]['SeriesName']}/{DocNum}"

            ord_sql = f"UPDATE `Invoice_invoice` SET `TaxDate` = '{str(opt['TaxDate'])}', `DocDueDate` = '{str(opt['DocDueDate'])}', `ContactPersonCode` = '{str(opt['ContactPersonCode'])}', `DiscountPercent` = '{str(discountPercent)}', `DocDate` = '{str(opt['DocDate'])}', `Comments` = '{str(Comments)}', `BPLID` = '{str(BPLID)}', `BPLName` = '{str(BPLName)}', `WTAmount` = '{str(WTAmount)}', `U_E_INV_NO` = '{str(U_E_INV_NO)}', `U_E_INV_Date` = '{str(U_E_INV_Date)}', `SalesPersonCode` = '{str(opt['SalesPersonCode'])}', `DocumentStatus` = '{str(opt['DocumentStatus'])}', `DocCurrency` = '{str(opt['DocCurrency'])}', `DocTotal` = '{str(opt['DocTotal'])}', `VatSum` = '{str(opt['VatSum'])}', `UpdateDate` = '{str(UpdateTime)}', `UpdateTime` = '{str(UpdateTime)}', `DeliveryCharge` = '{str(DeliveryCharge)}', `AdditionalCharges` = '{str(AdditionalCharges)}', `PaymentGroupCode` = '{str(opt['PaymentGroupCode'])}', `Series` = '{str(opt['Series'])}', `CancelStatus` = '{str(opt['CancelStatus'])}', `DocType` = '{str(opt['DocType'])}', `RoundingDiffAmount` = '{str(opt['RoundingDiffAmount'])}', `U_SignedQRCode` = '{str(opt['U_SignedQRCode'])}', `U_SignedInvoice` = '{str(opt['U_SignedInvoice'])}', `U_EWayBill` = '{str(opt['U_EWayBill'])}', `U_TransporterID` = '{str(U_TransporterID)}', `U_TransporterName` = '{str(U_TransporterName)}', `U_VehicalNo` = '{str(U_VehicalNo)}', `NumAtCard` = '{str(NumAtCard)}', `U_UNE_LRNo` = '{str(U_UNE_LRNo)}', `U_UNE_LRDate` = '{str(U_UNE_LRDate)}', `U_UNE_IRN` = '{str(IRNNo)}', `OriginalRefNo` = '{str(OriginalRefNo)}', `OriginalRefDate` = '{str(OriginalRefDate)}', `GSTTransactionType` = '{str(GSTTransactionType)}', `CNNo` = '{str(CNNo)}', `Address` = '{str(Address)}', `Address2` = '{str(Address2)}', `VATRegNum` = '{str(VATRegNum)}', `PaidToDateSys` = '{str(PaidToDateSys)}' WHERE `id` = '{InvoiceID}'"
        
            print(ord_sql)
            mycursor.execute(ord_sql)
            mydb.commit()
            
            add = opt['AddressExtension']                    
            ShipToStreet    = str(add['ShipToStreet']).replace("'", "\\")
            ShipToBlock     = str(add['ShipToBlock']).replace("'", "\\")
            ShipToBuilding  = str(add['ShipToBuilding']).replace("'", "\\")
            ShipToCity      = str(add['ShipToCity']).replace("'", "\\")
            ShipToZipCode   = str(add['ShipToZipCode']).replace("'", "\\")
            ShipToCounty    = str(add['ShipToCounty']).replace("'", "\\")
            ShipToState     = str(add['ShipToState']).replace("'", "\\")
            ShipToCountry   = str(add['ShipToCountry']).replace("'", "\\")
            ShipToAddress2  = str(add['ShipToAddress2']).replace("'", "\\")
            ShipToAddress3  = str(add['ShipToAddress3']).replace("'", "\\")
            BillToStreet    = str(add['BillToStreet']).replace("'", "\\")
            BillToBlock     = str(add['BillToBlock']).replace("'", "\\")
            BillToBuilding  = str(add['BillToBuilding']).replace("'", "\\")
            BillToCity      = str(add['BillToCity']).replace("'", "\\")
            BillToZipCode   = str(add['BillToZipCode']).replace("'", "\\")
            BillToCounty    = str(add['BillToCounty']).replace("'", "\\")
            BillToState     = str(add['BillToState']).replace("'", "\\")
            BillToCountry   = str(add['BillToCountry']).replace("'", "\\")
            BillToAddress2  = str(add['BillToAddress2']).replace("'", "\\")
            BillToAddress3  = str(add['BillToAddress3']).replace("'", "\\")
            PlaceOfSupply   = str(add['PlaceOfSupply']).replace("'", "\\")
            PurchasePlaceOfSupply = str(add['PurchasePlaceOfSupply']).replace("'", "\\")
            U_SCOUNTRY      = ""
            U_SSTATE        = ""
            U_SHPTYPB       = ""
            U_BSTATE        = ""
            U_BCOUNTRY      = ""
            U_SHPTYPS       = ""

            add_sql = f"UPDATE `Invoice_addressextension` SET `ShipToStreet` = '{ShipToStreet}', `ShipToBlock` = '{ShipToBlock}', `ShipToBuilding` = '{ShipToBuilding}', `ShipToCity` = '{ShipToCity}', `ShipToZipCode` = '{ShipToZipCode}', `ShipToCounty` = '{ShipToCounty}', `ShipToState` = '{ShipToState}', `ShipToCountry` = '{ShipToCountry}', `ShipToAddress2` = '{ShipToAddress2}', `ShipToAddress3` = '{ShipToAddress3}', `BillToStreet` = '{BillToStreet}', `BillToBlock` = '{BillToBlock}', `BillToBuilding` = '{BillToBuilding}', `BillToCity` = '{BillToCity}', `BillToZipCode` = '{BillToZipCode}', `BillToCounty` = '{BillToCounty}', `BillToState` = '{BillToState}', `BillToCountry` = '{BillToCountry}', `BillToAddress2` = '{BillToAddress2}', `BillToAddress3` = '{BillToAddress3}', `PlaceOfSupply` = '{PlaceOfSupply}', `PurchasePlaceOfSupply` = '{PurchasePlaceOfSupply}', `U_SCOUNTRY` = '{U_SCOUNTRY}', `U_SSTATE` = '{U_SSTATE}', `U_SHPTYPB` = '{U_SHPTYPB}', `U_BSTATE` = '{U_BSTATE}', `U_BCOUNTRY` = '{U_BCOUNTRY}', `U_SHPTYPS` = '{U_SHPTYPS}' WHERE InvoiceID = {InvoiceID}"
            print(add_sql)                
            mycursor.execute(add_sql)
            mydb.commit()

            itemCount = 0
            totalPrice = DocTotal
            for line in opt['DocumentLines']:
                lDiscountPercent = line['DiscountPercent']
                if str(lDiscountPercent) == 'None':
                    lDiscountPercent = 0.0
                
                BaseEntry = str(line['BaseEntry']) # sap order id
                TaxRate = str(line['TaxPercentagePerRow'])

                # tax igst cgst sgst
                taxDocLines = line['LineTaxJurisdictions']
                GSTRate = float(taxDocLines[0]['TaxRate'])
                if len(taxDocLines) > 1:
                    CGST = CGST + float(taxDocLines[0]['TaxAmount'])
                    SGST = SGST + float(taxDocLines[1]['TaxAmount'])
                else:
                    IGST = IGST + float(taxDocLines[0]['TaxAmount'])

                FreeText = str(line['FreeText']).replace("'","\\'")

                HSNEntry = str(line['HSNEntry'])
                SACEntry = str(line['SACEntry'])
                HSN = ""
                SAC = ""

                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                if HSNEntry != "None":
                    hsnAPIRsponse = requests.get(f"http://35.154.67.167:8000//Ledure/General/GetHSN.xsjs?DBName=LEDURE_LIVE_300323&AbsEntry={HSNEntry}", cookies=r.cookies, verify=False)
                    rsponseJson = json.loads(hsnAPIRsponse.text)
                    print(rsponseJson)
                    rsponseData = rsponseJson['value']
                    if len(rsponseData) > 0:
                        HSN = rsponseData[0]['HSN']
                elif SACEntry != "None":
                    sacAPIRsponse = requests.get(f"http://35.154.67.167:8000//Ledure/General/GetSacName.xsjs?DBName=LEDURE_LIVE_300323&AbsEntry={SACEntry}", cookies=r.cookies, verify=False)
                    rsponseJson = json.loads(sacAPIRsponse.text)
                    print(rsponseJson)
                    rsponseData = rsponseJson['value']
                    if len(rsponseData) > 0:
                        SAC = rsponseData[0]['SacName']
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                U_UTL_ITSBG = ''
                # line_sql = "INSERT INTO `Invoice_documentlines`(`LineNum`, `InvoiceID`, `Quantity`, `UnitPrice`, `DiscountPercent`, `ItemDescription`, `ItemCode`, `TaxCode`, `BaseEntry`, `TaxRate`, `UomNo`, `LineTotal`, `U_UTL_DIST`, `U_UTL_SP`, `U_UTL_DD`, `U_UTL_SD`, `U_UTL_TD`, `U_UTL_MRPI`, `U_RateType`,`MeasureUnit`, `HSNEntry`, `SACEntry`, `HSN`, `SAC` ,`U_UTL_ITSBG`) VALUES ('"+str(line['LineNum'])+"', '"+str(InvoiceID)+"', '"+str(line['Quantity'])+"', '"+str(line['UnitPrice'])+"', '"+str(lDiscountPercent)+"', '"+str(line['ItemDescription'])+"', '"+str(line['ItemCode'])+"', '"+str(line['TaxCode'])+"', '"+str(BaseEntry)+"', '"+str(TaxRate)+"', '"+str(line['UoMCode'])+"', '"+str(line['LineTotal'])+"','"+str(line['U_UTL_DIST'])+"','"+str(line['U_UTL_SP'])+"','"+str(line['U_UTL_DD'])+"','"+str(line['U_UTL_SD'])+"','"+str(line['U_UTL_TD'])+"','"+str(line['U_UTL_MRPI'])+"','"+str(line['U_RateType'])+"','"+str(line['MeasureUnit'])+"','"+str(HSNEntry)+"','"+str(SACEntry)+"','"+str(HSN)+"','"+str(SAC)+"', '"+str(U_UTL_ITSBG)+"');"
                line_sql = f"UPDATE `Invoice_documentlines` SET `Quantity` = '{str(line['Quantity'])}', `UnitPrice` = '{str(line['UnitPrice'])}', `DiscountPercent` = '{str(lDiscountPercent)}', `ItemDescription` = '{str(line['ItemDescription'])}', `ItemCode` = '{str(line['ItemCode'])}', `TaxCode` = '{str(line['TaxCode'])}', `BaseEntry` = '{str(BaseEntry)}', `TaxRate` = '{str(TaxRate)}', `UomNo` = '{str(line['UoMCode'])}', `LineTotal` = '{str(line['LineTotal'])}', `U_UTL_DIST` = '{str(line['U_UTL_DIST'])}', `U_UTL_SP` = '{str(line['U_UTL_SP'])}', `U_UTL_DD` = '{str(line['U_UTL_DD'])}', `U_UTL_SD` = '{str(line['U_UTL_SD'])}', `U_UTL_TD` = '{str(line['U_UTL_TD'])}', `U_UTL_MRPI` = '{str(line['U_UTL_MRPI'])}', `U_RateType` = '{str(line['U_RateType'])}', `MeasureUnit` = '{str(line['MeasureUnit'])}', `HSNEntry` = '{str(HSNEntry)}', `SACEntry` = '{str(SACEntry)}', `HSN` = '{str(HSN)}', `SAC`  = '{str(SAC)}', `U_UTL_ITSBG` = '{str(U_UTL_ITSBG)}' WHERE `InvoiceID` = '{InvoiceID}' AND `LineNum` = '{str(line['LineNum'])}'"

                print(line_sql)
                mycursor.execute(line_sql)
                mydb.commit()
                itemCount = itemCount+1
            # endfor
            sqlInvUpd = f"UPDATE `Invoice_invoice` SET `IGST` = '{IGST}', `CGST` = '{CGST}', `SGST` = '{SGST}', `GSTRate` = '{GSTRate}' WHERE `id` = '{InvoiceID}'"
            print(sqlInvUpd)
            mycursor.execute(sqlInvUpd)
            mydb.commit()
            bpid = mycursor.lastrowid
        # endif
    # endfor        
# endfor

