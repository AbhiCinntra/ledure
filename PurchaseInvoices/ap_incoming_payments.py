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
    password='F5GB?d4R#SW@r',
    # password='$Bridge@2022#',
    database='ledure_dev',
    # port = '8889'
)
mycursor = mydb.cursor(dictionary=True, buffered=True)

print("<><><><><><><><><><><>><><><><><><")
print("===== Login SAP ====")
data = {"CompanyDB": "LEDURE_LIVE_300323", "Password": "1020", "UserName": "PRO001", "SessionId": "d802ea02-512e-11ee-8000-0a427ed74412", "at": "2023-09-12 11:10:12", "sapurl": "https://35.154.67.167:50000/b1s/v1"}
r = requests.post(data['sapurl']+'/Login', data=json.dumps(data), verify=False)
print(r)
# currentDate = '2023-04-24'
# res = requests.get(data['sapurl']+'/VendorPayments?$filter=DocDate eq '+str(currentDate)+'', headers={'Authorization': "Bearer "+data['SessionId']+""}, verify=False)
# res = requests.get(data['sapurl']+'/VendorPayments?$filter=DocDate gt '+str(currentDate), cookies=r.cookies, verify=False)
# opts = json.loads(res.text)
# print("Total Fetched Row: ", len(opts['value']))

lastDocEntry = 0
mycursor.execute("SELECT * FROM `PurchaseInvoices_vendorpayments` ORDER BY `id` desc LIMIT 1")
entryData = mycursor.fetchall()
if len(entryData) > 0:
    lastDocEntry = entryData[0]['DocEntry']
    print(lastDocEntry)

skip=0
# for i in range(count):
while skip != "":

    sapAPIUrl = f"/VendorPayments?$filter = DocEntry gt {lastDocEntry}&$skip = {skip}"
    print(sapAPIUrl)
    res = requests.get(data['sapurl']+sapAPIUrl, cookies=r.cookies, verify=False)
    # print(res.text)
    opts = json.loads(res.text)

    for opt in opts['value']:
        # try:
        DocEntry = opt['DocEntry']
        print("DocEntry: ", DocEntry)

        checkPaymentQuery = f"select * from PurchaseInvoices_vendorpayments WHERE DocEntry = '{DocEntry}'"
        print(checkPaymentQuery)
        mycursor.execute(checkPaymentQuery)
        if mycursor.rowcount == 0:
            DocNum          = str(opt['DocNum'])
            DocType         = urllib.parse.quote(str(opt['DocType']))
            DocDate         = str(opt['DocDate'])
            CardCode        = urllib.parse.quote(str(opt['CardCode']))
            CardName        = urllib.parse.quote(str(opt['CardName']))
            # Address         = urllib.parse.quote(str(opt['Address']))
            Address         = ''
            DocCurrency     = urllib.parse.quote(str(opt['DocCurrency']))
            CheckAccount    = urllib.parse.quote(str(opt['CheckAccount']))
            TransferAccount = urllib.parse.quote(str(opt['TransferAccount']))
            TransferSum     = float(opt['TransferSum'])
            TransferDate    = str(opt['TransferDate'])
            Series          = str(opt['Series'])
            DocEntry        = str(opt['DocEntry'])
            DueDate         = str(opt['DueDate'])
            BPLID           = str(opt['BPLID'])
            BPLName         = urllib.parse.quote(str(opt['BPLName']))
            Comments         = urllib.parse.quote(str(opt['Remarks']))
            TransferReference = urllib.parse.quote(str(opt['TransferReference']))
            JournalRemarks  = str(opt['JournalRemarks'])
            print("CardName: ", CardName)

            # print("TransferSum", TransferSum)
            if TransferSum == 0.0:
                print('in if')
                # if len(opt['PaymentInvoices']) > 0:
                #     for line in opt['PaymentInvoices']:
                #         TransferSum = TransferSum + float(line['SumApplied'])
                
                if len(opt['PaymentCreditCards']) > 0:
                    for line in opt['PaymentCreditCards']:
                        TransferSum = TransferSum + float(line['CreditSum'])
                
                if len(opt['PaymentChecks']) > 0:
                    for line in opt['PaymentChecks']:
                        TransferSum = TransferSum + float(line['CheckSum'])
                
                # if len(opt['PaymentAccounts']) > 0:
                #     for line in opt['PaymentAccounts']:
                #         TransferSum = TransferSum + float(line['SumPaid'])
                TransferSum = TransferSum + float(opt['CashSumSys'])

                print("TransferSum", TransferSum)
                # exit()
            else:
                print("in else", TransferSum)
                
            add_incommingPayemnt = f'INSERT INTO `PurchaseInvoices_vendorpayments`(`DocEntry`, `CardCode`, `CardName`, `DocDate`, `TransferAccount`, `TransferSum`, `TransferDate`, `TransferReference`, `Address`, `BPLID`, `BPLName`, `CheckAccount`, `DocCurrency`, `DocNum`, `DocType`, `DueDate`, `Series`, `Comments`, `JournalRemarks`) VALUES("{DocEntry}", "{CardCode}", "{CardName}", "{DocDate}", "{TransferAccount}", "{TransferSum}", "{TransferDate}", "{TransferReference}", "{Address}", "{BPLID}", "{BPLName}", "{CheckAccount}", "{DocCurrency}", "{DocNum}", "{DocType}", "{DueDate}", "{Series}", "{Comments}", "{JournalRemarks}")'
            print(add_incommingPayemnt) 
            mycursor.execute(add_incommingPayemnt)
            mydb.commit()
            VendorPaymentsId = mycursor.lastrowid

                
            for line in opt['PaymentInvoices']:

                # # Check Invoice Exist or not
                # docSelectQuery = f"select * from Invoice_invoice WHERE DocEntry = '{InvoiceDocEntry}'"
                # print(docSelectQuery)
                # mycursor.execute(docSelectQuery)
                # mycursor.fetchall()
                # if mycursor.rowcount != 0:

                LineNum = str(line['LineNum'])
                InvoiceDocEntry = str(line['DocEntry'])
                SumApplied = str(line['SumApplied'])
                AppliedFC = str(line['AppliedFC'])
                AppliedSys = str(line['AppliedSys'])
                DiscountPercent = str(line['DiscountPercent'])
                TotalDiscount = str(line['TotalDiscount'])
                TotalDiscountFC = str(line['TotalDiscountFC'])
                TotalDiscountSC = str(line['TotalDiscountSC'])
                    
                add_incommingPayemntInvoice = f'INSERT INTO `PurchaseInvoices_vendorpaymentsinvoices`(`LineNum`, `InvoiceDocEntry`, `SumApplied`, `AppliedFC`, `AppliedSys`, `DiscountPercent`, `TotalDiscount`, `TotalDiscountFC`, `TotalDiscountSC`, `VendorPaymentsId`, `DocDate`) VALUES("{LineNum}", "{InvoiceDocEntry}", "{SumApplied}", "{AppliedFC}", "{AppliedSys}", "{DiscountPercent}", "{TotalDiscount}", "{TotalDiscountFC}", "{TotalDiscountSC}", "{VendorPaymentsId}", "{DocDate}")'
                print(add_incommingPayemntInvoice) 
                mycursor.execute(add_incommingPayemntInvoice)
                mydb.commit()
                
            # endfor
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
