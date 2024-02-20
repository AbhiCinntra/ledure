# >>>>>>>>>>>>>>>>>>>>>>>
# */10 * * * * /usr/bin/python3 /home/www/b2b/ledure_dev/bridge/BusinessPartner/sync_bp_every_five_minute.py
# >>>>>>>>>>>>>>>>>>>>>>>
import mysql.connector
import calendar
import requests, json
import time
import math
from datetime import date, datetime
import sys, os

def none(inp):
    inp = str(inp)
    if inp.lower()=="none":
        return "";
    else:
        return inp

currentDate = date.today()
currentDay = calendar.day_name[currentDate.weekday()]  # this will return the day of a week
currentTime = datetime.today().strftime("%I:%M %p")
currentDateTime = f"{currentDate} {currentTime}"
serverDateTime = datetime.now()

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def log_error(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"ERROR - {timestamp} - {message}\n"

    filename = "/home/www/b2b/ledure_dev/bridge/LogFiles/bp_cronjob_error_log.txt"
    # filename = "je_cronjob_error_log.txt"
    if not os.path.exists(filename):
        with open(filename, "w") as error_log_file:
            error_log_file.write(log_entry)
    else:
        with open(filename, "a") as error_log_file:
            error_log_file.write("\n" +log_entry)
    # endif
# endif
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# if True:
try:
    log_error('Sync Start')
    
    # print('>>>>>>>>>>>> Ledure Prod JE.py <<<<<<<<<<<<<<<<<<<<')
    # print('>>>>>>>>>>>> Ledure Prod JE.py <<<<<<<<<<<<<<<<<<<<')
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        # password='root',
        # database='ledure_pre'
        password='F5GB?d4R#SW@r',
        database='ledure_dev'
        # port = '8889',
    )
    mycursor = mydb.cursor(dictionary=True, buffered=True)

    # print("<><><><><><><><><><><>><><><><><><")
    # print("===== Login SAP ====")
    data = {"CompanyDB": "LEDURE_LIVE_300323", "Password": "1020", "UserName": "PRO001", "SessionId": "d802ea02-512e-11ee-8000-0a427ed74412", "at": "2023-09-12 11:10:12", "sapurl": "https://35.154.67.167:50000/b1s/v1"}
    r = requests.post(data['sapurl']+'/Login', data=json.dumps(data), verify=False)
    # # print(r)

    lastEntryNumber = 0
    mycursor.execute("SELECT * FROM `JournalEntries_journalentries` ORDER BY `id` desc LIMIT 1")
    entryData = mycursor.fetchall()
    if len(entryData) > 0:
        lastEntryNumber = entryData[0]['JdtNum']
        # print(lastEntryNumber)

    skip=0
    while skip != "":
        tempPrint = 0

        baseUrl = f"/BusinessPartners?$filter = CreateDate ge '{str(currentDate)}'"
        # print("><><><><><><><", data['sapurl']+baseUrl)
        res = requests.get(data['sapurl']+baseUrl, cookies=r.cookies, headers={"Prefer":"odata.maxpagesize=100"}, verify=False)
        # print(res.text)
        opts = json.loads(res.text)
        for bp in opts['value']:
            print('-----Business Partner---', str(bp['CardCode']))
            bpcode = bp['CardCode']
            CreatedBy = 1
            FreeDelivery = 1
            Unit       = bp['BPBranchAssignment'][0]['BPLID']
            CardCode   = (bp['CardCode'])
            CardName   = str(bp['CardName']).replace("'", "&sbquo;")
            Industry   = (bp['Industry'])
            CardType   = (bp['CardType'])
            Website    = (bp['Website'])
            EmailAddress = (bp['EmailAddress'])
            Phone1     = (bp['Phone1'])
            DiscountPercent = (bp['DiscountPercent'])
            Currency   = (bp['Currency'])
            IntrestRatePercent = (bp['IntrestRatePercent'])
            CommissionPercent = (bp['CommissionPercent'])
            Notes      = (bp['Notes'])
            PayTermsGrpCode = (bp['PayTermsGrpCode'])
            CreditLimit = (bp['CreditLimit'])
            AttachmentEntry = (bp['AttachmentEntry'])
            SalesPersonCode = (bp['SalesPersonCode'])
            ContactPerson = (bp['ContactPerson'])
            CreateDate = (bp['CreateDate'])
            CreateTime = (bp['CreateTime'])
            UpdateDate = (bp['UpdateDate'])
            UpdateTime = (bp['UpdateTime'])
            PriceListNum = bp['PriceListNum']
            GroupCode = bp['GroupCode']
            U_U_UTL_Zone = bp['U_U_UTL_Zone']
            U_U_UTL_DEPT = bp['U_U_UTL_DEPT']
            U_U_UTL_EXEC = bp['U_U_UTL_EXEC']
            U_U_UTL_DIRC = bp['U_U_UTL_DIRC']
            LinkedBusinessPartner = str(bp['LinkedBusinessPartner'])
            
            Link = "Sales Executive"
            Valid = str(bp['Valid']) # active status

            # if Valid == 'tNO':
            #     # print('inactive BP')
            #     continue

            updatedCreditLimit = float(bp['CreditLimit'])
            CurrentAccountBalance = bp['CurrentAccountBalance']
            OpenDeliveryNotesBalance = bp['OpenDeliveryNotesBalance']
            OpenOrdersBalance = bp['OpenOrdersBalance']
            OpenChecksBalance = bp['OpenChecksBalance'] # not in currently used
            totalCreditLimitUsed = float(float(CurrentAccountBalance) + float(OpenDeliveryNotesBalance) + float(OpenOrdersBalance))
            newLeftCreditLimit = float(updatedCreditLimit - totalCreditLimitUsed)

            sql_select_bp = f"SELECT `id` FROM BusinessPartner_businesspartner WHERE CardCode = '{bpcode}'"
            print(sql_select_bp)
            mycursor.execute(sql_select_bp)
            bpData = mycursor.fetchall()
            if mycursor.rowcount != 1:
                
                sqlBp = f"INSERT INTO `BusinessPartner_businesspartner`(`CardCode`, `CardName`, `Industry`, `CardType`, `Website`, `EmailAddress`, `Phone1`, `DiscountPercent`, `Currency`, `IntrestRatePercent`, `CommissionPercent`, `Notes`, `PayTermsGrpCode`, `CreditLimit`, `AttachmentEntry`, `SalesPersonCode`, `ContactPerson`, `BPAddresses`, `U_PARENTACC`, `U_BPGRP`, `U_CONTOWNR`, `U_RATING`, `U_TYPE`, `U_ANLRVN`, `U_CURBAL`, `U_ACCNT`, `U_INVNO`, `U_LAT`, `U_LONG`, `CreateDate`, `CreateTime`, `UpdateDate`, `UpdateTime`, `U_LEADID`, `U_LEADNM`, `CustomerType`, `DeliveryMode`, `GroupType`, `PaymantMode`, `PriceCategory`, `Turnover`, `ACNumber`, `BankName`, `BeneficiaryName`, `IfscCode`, `TCS`, `Link`, `Unit`, `CreditLimitLeft`, `FreeDelivery`, `CreatedBy`, `CreatedFromSap`, `CurrentAccountBalance`,`OpenDeliveryNotesBalance`,`OpenOrdersBalance`,`OpenChecksBalance`, `GroupCode`,`U_U_UTL_Zone`,`U_U_UTL_DEPT`,`U_U_UTL_EXEC`,`U_U_UTL_DIRC`, `LinkedBusinessPartner`) VALUES ('{CardCode}','{CardName}','{Industry}','{CardType}','{Website}','{EmailAddress}','{Phone1}','{DiscountPercent}','{Currency}','{IntrestRatePercent}','{CommissionPercent}','{Notes}','{PayTermsGrpCode}','{CreditLimit}','{AttachmentEntry}','{SalesPersonCode}','{ContactPerson}','','','','','','','','','','','','', '{CreateDate}','{CreateTime}','{UpdateDate}','{UpdateTime}','','','','','','','{PriceListNum}','','','','','','No','{Link}','{Unit}','{newLeftCreditLimit}','{FreeDelivery}','{CreatedBy}', '1','{CurrentAccountBalance}','{OpenDeliveryNotesBalance}','{OpenOrdersBalance}','{OpenChecksBalance}','{GroupCode}','{U_U_UTL_Zone}','{U_U_UTL_DEPT}','{U_U_UTL_EXEC}','{U_U_UTL_DIRC}', '{LinkedBusinessPartner}')"
                # print(sqlBp)
                mycursor.execute(sqlBp)
                mydb.commit()
                bpid = mycursor.lastrowid
                # print("BP ID: "+str(bpid))

                # print('-----BPAddresses---')
                if len(bp['BPAddresses']) > 0:
                    # print(len(bp['BPAddresses']))
                    for branch in bp['BPAddresses']:
                        # print("BP Address ID: "+str(branch['AddressName']))

                        if int(branch['RowNum']) == 0:
                            sqlBPAddress = "INSERT INTO `BusinessPartner_bpaddresses`(`BPID`, `BPCode`, `AddressName`, `Street`, `Block`, `City`, `State`, `ZipCode`, `Country`, `AddressType`, `RowNum`, `U_SHPTYP`, `U_COUNTRY`, `U_STATE`, `District`, `GSTIN`, `GstType`) VALUES ('"+str(bpid)+"', '"+str(branch['BPCode']).replace("'", "&sbquo;")+"', '"+str(branch['AddressName']).replace("'", "&sbquo;")+"', '"+str(none(branch['Street'])).replace("'", "&sbquo;")+"', '"+str(none(branch['Block'])).replace("'", "&sbquo;")+"', '"+str(branch['City']).replace("'", "&sbquo;")+"', '"+str(branch['State'])+"', '"+str(branch['ZipCode'])+"', '"+str(branch['Country'])+"', '"+str(branch['AddressType']).replace("'", "&sbquo;")+"', '"+str(branch['RowNum'])+"', '','','','', '"+str(branch['GSTIN'])+"', '"+str(branch['GstType'])+"')"
                            # print(sqlBPAddress)
                            mycursor.execute(sqlBPAddress)
                            mydb.commit()
                        else:
                            # print('-----BPBranch---')
                            branch_sql = "INSERT INTO `BusinessPartner_bpbranch`(`BPID`, `RowNum`, `BPCode`, `BranchName`, `AddressName`, `AddressName2`, `AddressName3`, `BuildingFloorRoom`, `Street`, `Block`, `County`, `City`, `State`, `ZipCode`, `Country`, `AddressType`, `Phone`, `Fax`, `Email`, `TaxOffice`, `GSTIN`, `GstType`, `ShippingType`, `PaymentTerm`, `CurrentBalance`, `CreditLimit`, `Lat`, `Long`, `Status`, `Default`, `U_SHPTYP`, `U_COUNTRY`, `U_STATE`, `CreateDate`, `CreateTime`, `UpdateDate`, `UpdateTime`, `District`) VALUES ('"+str(bpid)+"', '"+str(branch['RowNum'])+"', '"+str(branch['BPCode'])+"', '', '"+str(branch['AddressName']).replace("'", "&sbquo;")+"', '"+str(branch['AddressName2']).replace("'", "&sbquo;")+"', '"+str(branch['AddressName3']).replace("'", "&sbquo;")+"', '"+str(branch['BuildingFloorRoom']).replace("'", "&sbquo;")+"', '"+str(none(branch['Street'])).replace("'", "&sbquo;")+"', '"+str(none(branch['Block'])).replace("'", "&sbquo;")+"', '"+str(branch['County']).replace("'", "&sbquo;")+"', '"+str(branch['City']).replace("'", "&sbquo;")+"', '"+str(branch['State']).replace("'", "&sbquo;")+"', '"+str(branch['ZipCode'])+"', '"+str(branch['Country'])+"', '"+str(branch['AddressType']).replace("'", "&sbquo;")+"', '','','', '"+str(branch['TaxOffice']).replace("'", "&sbquo;")+"', '"+str(branch['GSTIN'])+"', '"+str(branch['GstType'])+"', '','','','','', '', 1, 0,'','','', '"+str(branch['CreateDate'])+"', '"+str(branch['CreateTime'])+"', '', '', '');"
                            # print(branch_sql)
                            mycursor.execute(branch_sql)
                            mydb.commit()

                # print('-----ContactEmployees---')
                if len(bp['ContactEmployees']) > 0:
                    # print(len(bp['ContactEmployees']))
                    for emp in bp['ContactEmployees']:
                        # print("Title : "+str(emp['Title']))
                        emp_sql = "INSERT INTO `BusinessPartner_bpemployee` (`Title`, `FirstName`, `MiddleName`, `LastName`, `Position`, `Address`, `MobilePhone`, `Fax`, `E_Mail`, `Remarks1`, `InternalCode`, `DateOfBirth`, `Gender`, `Profession`, `CardCode`, `U_BPID`, `U_BRANCHID`, `U_NATIONALTY`, `CreateDate`, `CreateTime`, `UpdateDate`, `UpdateTime`) VALUES ('"+str(emp['Title']).replace("'", "&sbquo;")+"', '"+str(emp['Name']).replace("'", "&sbquo;")+"', '"+str(emp['MiddleName']).replace("'", "&sbquo;")+"', '"+str(emp['LastName']).replace("'", "&sbquo;")+"', '"+str(emp['Position'])+"', '"+str(emp['Address']).replace("'", "&sbquo;")+"', '"+str(emp['MobilePhone'])+"', '"+str(emp['Fax'])+"', '"+str(emp['E_Mail'])+"', '"+str(emp['Remarks1'])+"', '"+str(emp['InternalCode'])+"', '"+str(emp['DateOfBirth'])+"', '"+str(emp['Gender'])+"', '"+str(emp['Profession'])+"','"+str(bpcode)+"', '"+str(bpid)+"', '', '', '"+str(emp['CreateDate'])+"', '"+str(emp['CreateTime'])+"', '"+str(emp['UpdateDate'])+"', '"+str(emp['UpdateTime'])+"');"
                        # print(emp_sql)
                        mycursor.execute(emp_sql)
                        mydb.commit()
                    # endFor
                # endIf
            # endIf
        # end for

        if 'odata.nextLink' in opts:
            nextLink = opts['odata.nextLink']
            nextLink = nextLink.split("skip=")
            skip = str(nextLink[1]).strip()
        else:
            skip = ""
    # end while
    log_error('Sync End')
# >>>>>>>>>>>>>>>>>>>>
except Exception as e:
    error_message = f"Exception From BP Sync: {str(e)}"
    log_error(error_message)
    print(error_message)