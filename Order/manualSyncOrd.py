import requests, json
import time
import math
import mysql.connector

from datetime import datetime
from datetime import date, datetime, timedelta
import calendar
import sys, os
from requests.adapters import HTTPAdapter, Retry

currentDate = date.today()
currentDay = calendar.day_name[currentDate.weekday()]  # this will return the day of a week
currentTime = datetime.today().strftime("%I:%M %p")
currentDateTime = f"{currentDate} {currentTime}"
serverDateTime = datetime.now()

print('>>>>>>>>>>>> ledure_pre <<<<<<<<<<<<<<<<<<<<')
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    # password='root',
    password='F5GB?d4R#SW@r',
    # password='$Bridge@2022#',
    # database='ledure_pre'
    database='ledure_dev'
)
mycursor = mydb.cursor(dictionary=True, buffered=True)

print("<><><><><><><><><><><>><><><><><><")
print("===== Login SAP ====")
data = {"CompanyDB": "LEDURE_LIVE_300323", "Password": "1020", "UserName": "PRO001", "SessionId": "d802ea02-512e-11ee-8000-0a427ed74412", "at": "2023-09-12 11:10:12", "sapurl": "https://35.154.67.167:50000/b1s/v1"}
r = requests.post(data['sapurl']+'/Login', data=json.dumps(data), verify=False)
print(r)
tempDate = date.today() - timedelta(days=5)

lastDocEntry = 11661
# mycursor.execute("SELECT * FROM `Order_order` ORDER BY `id` desc LIMIT 1")
# entryData = mycursor.fetchall()
# if len(entryData) > 0:
#     lastDocEntry = entryData[0]['DocEntry']
#     print(lastDocEntry)

# if int(count) > 0:
if True:
    skip=0
    while skip != "":        
        # sapAPIUrl = f"/Orders?$filter = DocEntry eq {lastDocEntry}&$skip = {skip}"
        sapAPIUrl = f"/Orders?$filter = DocumentStatus eq 'bost_Open' and DocEntry ge {lastDocEntry}&$skip = {skip}"
        # sapAPIUrl = f"/Orders?$filter=DocumentStatus ne 'bost_Open' and UpdateDate ge {str(tempDate)}&$skip = {skip}"
        print(sapAPIUrl)
        res = requests.get(data['sapurl']+sapAPIUrl, cookies=r.cookies, verify=False)
        # print(res.text)
        opts = json.loads(res.text)
        for opt in opts['value']:
            DocEntry = opt['DocEntry']
            print("DocEntry: ", DocEntry)
        
            docSelectQuery = f"select * from Order_order WHERE DocEntry = '{DocEntry}'"
            print(docSelectQuery)
            mycursor.execute(docSelectQuery)
            ordDetails = mycursor.fetchall()
            if mycursor.rowcount == 1:
                # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                # 
                #                                       Update Order
                #   
                # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                OrderID = ordDetails[0]['id']    
                d = datetime.strptime(str(opt['DocTime']), "%H:%M:%S")
                DocTime = d.strftime("%I:%M:%S %p")

                e = datetime.strptime(str(opt['UpdateTime']), "%H:%M:%S")
                UpdateTime = e.strftime("%I:%M:%S %p")

                discountPercent = str(opt['DiscountPercent'])
                if str(discountPercent) == 'None':
                    discountPercent = 0.0

                
                CardCode = opt['CardCode']
                DeliveryCharge = 0
                AdditionalCharges = 0
                if len(opt['DocumentAdditionalExpenses']) !=0:
                    DeliveryCharge = opt['DocumentAdditionalExpenses'][0]['LineTotal']
                    AdditionalCharges = opt['DocumentAdditionalExpenses'][1]['LineTotal']

                # str(discountPercent)
                TaxDate         = opt['TaxDate']
                DocDueDate      = opt['DocDueDate']
                ContactPersonCode = opt['ContactPersonCode']
                DiscountPercent = discountPercent
                DocDate         = opt['DocDate']
                CardCode        = opt['CardCode']
                Comments        = opt['Comments']
                SalesPersonCode = opt['SalesPersonCode']
                DocumentStatus  = opt['DocumentStatus']
                DocCurrency     = opt['DocCurrency']
                DocTotal        = opt['DocTotal']
                CardName        = str(opt['CardName']).replace("'","\\'")
                VatSum          = opt['VatSum']
                CreationDate    = opt['CreationDate']
                DocEntry        = opt['DocEntry']
                CreateDate      = opt['CreationDate']
                CreateTime      = ""
                UpdateDate      = opt['UpdateDate']
                CancelStatus    = opt['CancelStatus']
                NetTotal        = 0.0
                AdditionalCharges = AdditionalCharges
                DeliveryCharge  = DeliveryCharge
                Unit            = opt['BPL_IDAssignedToInvoice']
                PayTermsGrpCode = opt['PaymentGroupCode']
                CreatedBy       = opt['SalesPersonCode']
                
                ord_sql = f"UPDATE `Order_order` SET `TaxDate` = '{TaxDate}',`DocDueDate` = '{DocDueDate}',`ContactPersonCode` = '{ContactPersonCode}',`DiscountPercent` = '{DiscountPercent}',`DocDate` = '{DocDate}', `Comments` = '{Comments}',`DocumentStatus` = '{DocumentStatus}',`DocCurrency` = '{DocCurrency}',`DocTotal` = '{DocTotal}',`VatSum` = '{VatSum}',`UpdateDate` = '{UpdateDate}',`UpdateTime` = '{UpdateTime}',`CancelStatus` = '{CancelStatus}', `NetTotal` = '{NetTotal}', `AdditionalCharges` = '{AdditionalCharges}', `DeliveryCharge` = '{DeliveryCharge}', `Unit` = '{Unit}',`PayTermsGrpCode` = '{PayTermsGrpCode}' WHERE `DocEntry` = '{DocEntry}'"
                print(ord_sql)
                mycursor.execute(ord_sql)
                mydb.commit()
                
                # add            = opt['AddressExtension']
                # ShipToBuilding = str(add['ShipToBuilding']).replace("'","\\'")
                # BillToBuilding = str(add['BillToBuilding']).replace("'","\\'")
                # ShipToStreet   = str(add['ShipToStreet']).replace("'","\\'")
                # BillToStreet   = str(add['BillToStreet']).replace("'","\\'")
                # ShipToState    = add['ShipToState']
                # BillToCity     = add['BillToCity']
                # ShipToCountry  = add['ShipToCountry']
                # BillToZipCode  = add['BillToZipCode']
                # BillToState    = add['BillToState']
                # ShipToZipCode  = add['ShipToZipCode']
                # ShipToCity     = add['ShipToCity']
                # BillToCountry  = add['BillToCountry']

                # update_address = f"UPDATE `Order_addressextension` SET `BillToBuilding` = '{BillToBuilding}',`ShipToState` = '{ShipToState}',`BillToCity` = '{BillToCity}',`ShipToCountry` = '{ShipToCountry}',`BillToZipCode` = '{BillToZipCode}',`ShipToStreet` = '{ShipToStreet}',`BillToState` = '{BillToState}',`ShipToZipCode` = '{ShipToZipCode}',`BillToStreet` = '{BillToStreet}',`ShipToBuilding` = '{ShipToBuilding}',`ShipToCity` = '{ShipToCity}',`BillToCountry` = '{BillToCountry}' WHERE `OrderID` = '{OrderID}'"
                
                # print(update_address)                
                # mycursor.execute(update_address)
                # mydb.commit()

                itemCount = 0
                totalPrice = DocTotal
                for line in opt['DocumentLines']:
                    print(line['Quantity'])
                    print(line['DiscountPercent'])
                    
                    lDiscountPercent = str(line['DiscountPercent'])
                    if str(lDiscountPercent) == 'None':
                        lDiscountPercent = 0.0

                    BaseEntry       = str(line['BaseEntry']) # sap order id
                    TaxRate         = str(line['TaxPercentagePerRow'])
                    FreeText        = str(line['FreeText']).replace("'","\\'")
                    LineNum         = line['LineNum']
                    Quantity        = line['Quantity']
                    UnitPrice       = line['UnitPrice']
                    DiscountPercent = lDiscountPercent
                    ItemDescription = line['ItemDescription']
                    ItemCode        = line['ItemCode']
                    TaxCode         = line['TaxCode']
                    UnitPriceown    = line['UnitPrice']
                    UnitWeight      = ""
                    UomNo           = ""
                    RemainingOpenQuantity = line['RemainingOpenQuantity']
                    OpenAmount      = line['OpenAmount']
                    LineTotal       = line['LineTotal']

                    docLineQuery = f"select * from Order_documentlines WHERE `OrderID` = '{OrderID}' AND `LineNum` = '{LineNum}'"
                    print(docLineQuery)
                    mycursor.execute(docLineQuery)
                    if mycursor.rowcount > 0:
                        line_sql = f"UPDATE `Order_documentlines` SET `Quantity` = '{Quantity}',`UnitPrice` = '{UnitPrice}',`DiscountPercent` = '{DiscountPercent}',`ItemDescription` = '{ItemDescription}',`ItemCode` = '{ItemCode}',`TaxCode` = '{TaxCode}',`FreeText` = '{FreeText}',`TaxRate` = '{TaxRate}',`UnitPriceown` = '{UnitPriceown}', `RemainingOpenQuantity` = '{RemainingOpenQuantity}', `OpenAmount` = '{OpenAmount}', `LineTotal` = '{LineTotal}' WHERE `OrderID` = '{OrderID}' AND `LineNum` = '{LineNum}'"
                        print(line_sql)
                        mycursor.execute(line_sql)
                        mydb.commit()
                        itemCount = itemCount + 1
                    else:
                        line_sql = f"INSERT INTO `Order_documentlines`(`LineNum`, `OrderID`, `Quantity`, `UnitPrice`, `DiscountPercent`, `ItemDescription`, `ItemCode`, `TaxCode`, `FreeText`, `UnitWeight`, `UomNo`, `TaxRate`, `UnitPriceown`, `RemainingOpenQuantity`, `OpenAmount`, `LineTotal`) VALUES ('{LineNum}', '{OrderID}', '{Quantity}', '{UnitPrice}', '{DiscountPercent}', '{ItemDescription}', '{ItemCode}', '{TaxCode}', '{FreeText}', '{UnitWeight}', '{UomNo}', '{TaxRate}', '{UnitPriceown}', '{RemainingOpenQuantity}', '{OpenAmount}', '{LineTotal}')"
                        print(line_sql)
                        mycursor.execute(line_sql)
                        mydb.commit()

                # end for
            # end if
            else:
                # continue
                # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                # 
                #                                           Insert Order
                #   
                # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                d = datetime.strptime(str(opt['DocTime']), "%H:%M:%S")
                DocTime = d.strftime("%I:%M:%S %p")

                e = datetime.strptime(str(opt['UpdateTime']), "%H:%M:%S")
                UpdateTime = e.strftime("%I:%M:%S %p")  
                
                discountPercent = opt['DiscountPercent']
                if str(discountPercent) == 'None':
                    discountPercent = 0.0

                CardCode = opt['CardCode']
                DeliveryCharge = 0
                AdditionalCharges = 0
                if len(opt['DocumentAdditionalExpenses']) !=0:
                    DeliveryCharge = opt['DocumentAdditionalExpenses'][0]['LineTotal']
                    AdditionalCharges = opt['DocumentAdditionalExpenses'][1]['LineTotal']

                # str(discountPercent)
                TaxDate         = opt['TaxDate']
                DocDueDate      = opt['DocDueDate']
                ContactPersonCode = opt['ContactPersonCode']
                DiscountPercent = discountPercent
                DocDate         = opt['DocDate']
                CardCode        = opt['CardCode']
                Comments        = opt['Comments']
                SalesPersonCode = opt['SalesPersonCode']
                DocumentStatus  = opt['DocumentStatus']
                DocCurrency     = opt['DocCurrency']
                DocTotal        = opt['DocTotal']
                CardName        = str(opt['CardName']).replace("'","\\'")
                VatSum          = opt['VatSum']
                CreationDate    = opt['CreationDate']
                DocEntry        = opt['DocEntry']
                CreateDate      = opt['CreationDate']
                CreateTime      = ""
                UpdateDate      = opt['UpdateDate']
                UpdateTime      = ""
                U_OPPID         = ""
                U_OPPRNM        = ""
                U_QUOTID        = ""
                U_QUOTNM        = ""
                CancelStatus    = opt['CancelStatus']
                NetTotal        = 0.0
                AdditionalCharges = AdditionalCharges
                DeliveryCharge  = DeliveryCharge
                DeliveryMode    = ""
                DeliveryTerm    = ""
                PaymentType     = ""
                TermCondition   = ""
                Unit            = opt['BPL_IDAssignedToInvoice']
                U_LAT           = ""
                U_LONG          = ""
                Link            = ""
                PayTermsGrpCode = opt['PaymentGroupCode']
                ApprovalStatus  = ""
                ApproverId      = ""
                FreeDelivery    = ""
                CreatedBy       = opt['SalesPersonCode']

                ord_sql = f"INSERT INTO `Order_order`(`TaxDate`, `DocDueDate`, `ContactPersonCode`, `DiscountPercent`, `DocDate`, `CardCode`, `Comments`, `SalesPersonCode`, `DocumentStatus`, `DocCurrency`, `DocTotal`, `CardName`, `VatSum`, `CreationDate`, `DocEntry`, `CreateDate`, `CreateTime`, `UpdateDate`, `UpdateTime`, `U_OPPID`, `U_OPPRNM`, `U_QUOTID`, `U_QUOTNM`, `CancelStatus`, `NetTotal`, `AdditionalCharges`, `DeliveryCharge`, `DeliveryMode`, `DeliveryTerm`, `PaymentType`, `TermCondition`, `Unit`, `U_LAT`, `U_LONG`, `Link`, `PayTermsGrpCode`, `ApprovalStatus`, `ApproverId`, `FreeDelivery`, `CreatedBy`) VALUES ('{TaxDate}','{DocDueDate}','{ContactPersonCode}','{DiscountPercent}','{DocDate}','{CardCode}','{Comments}','{SalesPersonCode}','{DocumentStatus}','{DocCurrency}','{DocTotal}','{CardName}','{VatSum}','{CreationDate}','{DocEntry}','{CreateDate}','{CreateTime}','{UpdateDate}','{UpdateTime}','{U_OPPID}','{U_OPPRNM}','{U_QUOTID}','{U_QUOTNM}','{CancelStatus}','{NetTotal}','{AdditionalCharges}','{DeliveryCharge}','{DeliveryMode}','{DeliveryTerm}','{PaymentType}','{TermCondition}','{Unit}','{U_LAT}','{U_LONG}','{Link}','{PayTermsGrpCode}','{ApprovalStatus}','{ApproverId}','{FreeDelivery}','{CreatedBy}')"
            
                print(ord_sql)
                mycursor.execute(ord_sql)
                mydb.commit()                
                OrderID = mycursor.lastrowid
                
                add            = opt['AddressExtension']
                U_SCOUNTRY     = ""
                U_SSTATE       = ""
                U_SHPTYPB      = ""
                U_BSTATE       = ""
                U_BCOUNTRY     = ""
                U_SHPTYPS      = ""
                
                ShipToBuilding = str(add['ShipToBuilding']).replace("'","\\'")
                BillToBuilding = str(add['BillToBuilding']).replace("'","\\'")
                ShipToStreet   = str(add['ShipToStreet']).replace("'","\\'")
                BillToStreet   = str(add['BillToStreet']).replace("'","\\'")
                ShipToState    = add['ShipToState']
                BillToCity     = add['BillToCity']
                ShipToCountry  = add['ShipToCountry']
                BillToZipCode  = add['BillToZipCode']
                BillToState    = add['BillToState']
                ShipToZipCode  = add['ShipToZipCode']
                ShipToCity     = add['ShipToCity']
                BillToCountry  = add['BillToCountry']
                U_SCOUNTRY     = ""
                U_SSTATE       = ""
                U_SHPTYPB      = ""
                U_BSTATE       = ""
                U_BCOUNTRY     = ""
                U_SHPTYPS      = ""
                BillToDistrict = ""
                ShipToDistrict = ""

                add_sql = f"INSERT INTO `Order_addressextension`(`OrderID`, `BillToBuilding`, `ShipToState`, `BillToCity`, `ShipToCountry`, `BillToZipCode`, `ShipToStreet`, `BillToState`, `ShipToZipCode`, `BillToStreet`, `ShipToBuilding`, `ShipToCity`, `BillToCountry`, `U_SCOUNTRY`, `U_SSTATE`, `U_SHPTYPB`, `U_BSTATE`, `U_BCOUNTRY`, `U_SHPTYPS`, `BillToDistrict`, `ShipToDistrict`) VALUES ('{OrderID}', '{BillToBuilding}', '{ShipToState}', '{BillToCity}', '{ShipToCountry}', '{BillToZipCode}', '{ShipToStreet}', '{BillToState}', '{ShipToZipCode}', '{BillToStreet}', '{ShipToBuilding}', '{ShipToCity}', '{BillToCountry}', '{U_SCOUNTRY}', '{U_SSTATE}', '{U_SHPTYPB}', '{U_BSTATE}', '{U_BCOUNTRY}', '{U_SHPTYPS}', '{BillToDistrict}', '{ShipToDistrict}')"
                print(add_sql)                
                mycursor.execute(add_sql)
                mydb.commit()

                itemCount = 0
                totalPrice = DocTotal
                for line in opt['DocumentLines']:
                    print(line['Quantity'])
                    print(line['DiscountPercent'])                   
                    
                    lDiscountPercent = opt['DiscountPercent']
                    if str(lDiscountPercent) == 'None':
                        lDiscountPercent = 0.0

                    BaseEntry = str(line['BaseEntry']) # sap order id
                    TaxRate = str(line['TaxPercentagePerRow'])

                    FreeText = str(line['FreeText']).replace("'","\\'")

                    LineNum = line['LineNum']
                    Quantity = line['Quantity']
                    UnitPrice = line['UnitPrice']
                    DiscountPercent = lDiscountPercent
                    ItemDescription = line['ItemDescription']
                    ItemCode = line['ItemCode']
                    TaxCode = line['TaxCode']
                    FreeText = str(line['FreeText']).replace("'","\\'")
                    UnitWeight = ""
                    UomNo = ""
                    TaxRate = str(line['TaxPercentagePerRow'])
                    UnitPriceown = line['UnitPrice']
                    RemainingOpenQuantity = line['RemainingOpenQuantity']
                    OpenAmount      = line['OpenAmount']
                    LineTotal      = line['LineTotal']

                    line_sql = f"INSERT INTO `Order_documentlines`(`LineNum`, `OrderID`, `Quantity`, `UnitPrice`, `DiscountPercent`, `ItemDescription`, `ItemCode`, `TaxCode`, `FreeText`, `UnitWeight`, `UomNo`, `TaxRate`, `UnitPriceown`, `RemainingOpenQuantity`, `OpenAmount`, `LineTotal`) VALUES ('{LineNum}', '{OrderID}', '{Quantity}', '{UnitPrice}', '{DiscountPercent}', '{ItemDescription}', '{ItemCode}', '{TaxCode}', '{FreeText}', '{UnitWeight}', '{UomNo}', '{TaxRate}', '{UnitPriceown}', '{RemainingOpenQuantity}', '{OpenAmount}', '{LineTotal}')"

                    print(line_sql)
                    mycursor.execute(line_sql)
                    mydb.commit()
                    itemCount = itemCount+1
        # end for             

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

