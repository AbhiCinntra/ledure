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

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

currentDate = date.today()
currentDay = calendar.day_name[currentDate.weekday()]  # this will return the day of a week
currentTime = datetime.today().strftime("%I:%M %p")
currentDateTime = f"{currentDate} {currentTime}"
serverDateTime = datetime.now()

print('>>>>>>>>>>>> Ledure Pre <<<<<<<<<<<<<<<<<<<<')
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    # password='root',
    password='$Bridge@2022#',
    # password='F5GB?d4R#SW@r',
    database='ledure_pre',
    # port = '8889',
)
mycursor = mydb.cursor(dictionary=True, buffered=True)

print("<><><><><><><><><><><>><><><><><><")
print("===== Login SAP ====")
data = { "CompanyDB": "LEDURE_LIVE_300323", "Password": "L!l@364%$", "UserName": "uneecloud\\led.manager", "SessionId": "7c85460c-c15a-11ed-8000-005056a40bab", "at": "2023-03-13 10:19:30", "sapurl": "https://analytics103u.uneecloud.com:50000/b1s/v1" }
r = requests.post(data['sapurl']+'/Login', data=json.dumps(data), verify=False)
# print(r)

# currentDate = '2023-03-28'
# count = requests.get(data['sapurl']+'/JournalEntries/$count?$filter=UpdateDate ge '+str(currentDate)+'', headers={'Authorization': "Bearer "+data['SessionId']+""}, verify=False).text
# invCount = requests.get(data['sapurl']+'/JournalEntries/$count?$orderby = Number desc', cookies=r.cookies, verify=False).text
# print("invCount", invCount)
# invCount = 20
# count the number if loop run, each one skip 20 values
# count = math.ceil(int(invCount)/20)
# print(count)

lastEntryNumber = 0
# mycursor.execute("SELECT * FROM `JournalEntries_journalentries` ORDER BY `id` desc LIMIT 1")
# entryData = mycursor.fetchall()
# if len(entryData) > 0:
#     lastEntryNumber = entryData[0]['JdtNum']
#     print(lastEntryNumber)

if True:
    skip=0
    # for i in range(count):
    while skip != "":
        tempPrint = 0

        # dateFilter = '2023-06-09'
        # baseUrl = f"/JournalEntries?$orderby= JdtNum asc&$filter = ReferenceDate ge '{dateFilter}'&$skip={skip}"

        baseUrl = f"/JournalEntries?$orderby= JdtNum asc&$filter = JdtNum ge {lastEntryNumber}&$skip={skip}"
        res = requests.get(data['sapurl']+baseUrl, cookies=r.cookies, headers={"Prefer":"odata.maxpagesize=100"}, verify=False)
        # print(res.text)
        opts = json.loads(res.text)
        tempPrint = opts
                
        # print(opts['odata.metadata'])
        for opt in opts['value']:
            Number          = opt['Number']
            JdtNum          = opt['JdtNum']
            Original        = opt['Original']
            # Reference       = opt['Reference']
            ReferenceDate   = opt['ReferenceDate']
            Number          = opt['Number']
            Memo            = str(opt['Memo']).replace("'","").replace('\\', '')
            TransactionCode = opt['TransactionCode']
            TaxDate         = opt['TaxDate']
            U_UNE_Narration = str(opt['U_UNE_Narration']).replace("'","").replace('\\', '')
            U_Cancel        = opt['U_Cancel']

            ReconSum        = 0

            OriginalJournal = ""
            if 'OriginalJournal' in opt:
                OriginalJournal = opt['OriginalJournal']
            
            # from row level 
            ShortName = opt['JournalEntryLines'][0]['ShortName']
            ContraAccount = opt['JournalEntryLines'][0]['ContraAccount']

            entryList = f"('{ShortName}', '{ContraAccount}')"

            docSelectQuery = f"select * from JournalEntries_journalentries WHERE JdtNum = '{JdtNum}'"
            print(docSelectQuery)
            mycursor.execute(docSelectQuery)
            jeDetails = mycursor.fetchall()
            if mycursor.rowcount == 0:
                JournalEntryLines = opt['JournalEntryLines']
                bpSelectQuery = f"select * from `BusinessPartner_businesspartner` WHERE `CardCode` in{entryList}"
                # print(bpSelectQuery)
                mycursor.execute(bpSelectQuery)
                if mycursor.rowcount > 0:
                    # print("JdtNum ", JdtNum)
                    # print("#found", ShortName)
                    CNNo = JdtNum
                    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                    seriesNameURL = f"http://65.2.148.88:8000/Ledure/General/SeriesName.xsjs?DBName=LEDURE_LIVE_300323&DocEntry={JdtNum}&ObjType=30"
                    # print(seriesNameURL)
                    seriesNameResponse = requests.get(seriesNameURL, cookies=r.cookies, verify=False)
                    seriesNameJson = json.loads(seriesNameResponse.text)
                    seriesNameData = seriesNameJson['value']
                    TransType = ""
                    if len(seriesNameData) > 0:
                        IRNNo = seriesNameData[0]['IRNNo']
                        CNNo = f"{seriesNameData[0]['SeriesName']}/{JdtNum}"
                        TransType = seriesNameData[0]['TransType']
                    
                    jeType = {'-3':'BC', '-2':'OB', '13':'IN', '14':'CN', '15':'DN', '16':'RE', '18':'PU', '19':'PU', '20':'PD', '21':'PR', '24':'RC', '25':'DP', '30':'JE', '46':'PS', '57':'CP', '58':'ST', '59':'SI', '60':'SO', '67':'67', '69':'IF', '76':'DD', '162':'MR', '182':'BT', '202':'PW', '203':'DT', '321': 'JR'}
                    DocType = jeType[TransType]

                    ord_sql = f"INSERT INTO `JournalEntries_journalentries`(`JdtNum`, `Original`, `OriginalJournal`, `ReferenceDate`, `Number`, `Memo`, `TransactionCode`, `TaxDate`, `U_UNE_Narration`, `CNNo`, `DocType`, `U_Cancel`) VALUES ('{JdtNum}','{Original}','{OriginalJournal}', '{ReferenceDate}', '{Number}' ,'{Memo}' ,'{TransactionCode}' ,'{TaxDate}' ,'{U_UNE_Narration}', '{CNNo}', '{DocType}', '{U_Cancel}')"
                    print(ord_sql)
                    mycursor.execute(ord_sql)
                    mydb.commit()                
                    JournalEntriesId = mycursor.lastrowid
                    lineCount = 0
                    for line in JournalEntryLines:
                        Line_ID = line['Line_ID']
                        AccountCode = line['ContraAccount']
                        Debit = line['Debit']
                        Credit = line['Credit']
                        DueDate = line['DueDate']
                        ShortName = str(line['ShortName']).replace("'","").replace('\\', '')
                        ContraAccount = line['ContraAccount']
                        LineMemo = str(line['LineMemo']).replace("'","").replace('\\', '')
                        ReferenceDate1 = line['ReferenceDate1']
                        Reference1 = line['Reference1']

                        Reference2 = str(line['Reference2']).replace("'","").replace('\\', '')
                        BPLID = line['BPLID']
                        BPLName = str(line['BPLName']).replace("'","").replace('\\', '')

                        AccountName = ""
                        mycursor.execute(f"SELECT * FROM `Company_glaccounts` WHERE `Code` = '{AccountCode}'")
                        jeData = mycursor.fetchall()
                        if len(jeData) > 0:
                            AccountName = jeData[0]['Name']
                        else:
                            mycursor.execute(f"select `id`, `CardCode`, `CardName` from `BusinessPartner_businesspartner` WHERE `CardCode` = '{AccountCode}'")
                            bpData = mycursor.fetchall()
                            if len(bpData) > 0:
                                AccountName = bpData[0]['CardName']

                        line_sql = f"INSERT INTO `JournalEntries_journalentrylines`(`JournalEntriesId`, `Line_ID`, `AccountCode`, `Debit`, `Credit`, `DueDate`, `ShortName`, `ContraAccount`, `LineMemo`, `ReferenceDate1`, `Reference1`, `Reference2`, `BPLID`, `BPLName`, `AccountName`, `ReconSum`) VALUES ('{JournalEntriesId}','{Line_ID}','{AccountCode}','{Debit}','{Credit}','{DueDate}','{ShortName}','{ContraAccount}','{LineMemo}','{ReferenceDate1}','{Reference1}','{Reference2}','{BPLID}','{BPLName}', '{AccountName}', '{ReconSum}')"

                        # print(line_sql)
                        mycursor.execute(line_sql)
                        mydb.commit()
                            
                    # end for
                # end if
            # end if
            else:

                JournalEntriesId = jeDetails[0]['id']
                JournalEntryLines = opt['JournalEntryLines']

                sqlJE = f"UPDATE `JournalEntries_journalentries` SET `Original` = '{Original}',`OriginalJournal` = '{OriginalJournal}',`ReferenceDate` = '{ReferenceDate}',`Number` = '{Number}',`Memo` = '{Memo}',`TransactionCode` = '{TransactionCode}',`TaxDate` = '{TaxDate}',`U_UNE_Narration` = '{U_UNE_Narration}', `U_Cancel` = '{U_Cancel}' WHERE JdtNum = '{JdtNum}'"
                # print(sqlJE)
                mycursor.execute(sqlJE)
                mydb.commit()

                for line in JournalEntryLines:
                    Line_ID = line['Line_ID']
                    AccountCode = line['ContraAccount']
                    Debit = line['Debit']
                    Credit = line['Credit']
                    DueDate = line['DueDate']
                    ShortName = str(line['ShortName']).replace("'","").replace('\\', '')
                    ContraAccount = line['ContraAccount']
                    LineMemo = str(line['LineMemo']).replace("'","").replace('\\', '')
                    ReferenceDate1 = line['ReferenceDate1']
                    Reference1 = line['Reference1']

                    Reference2 = str(line['Reference2']).replace("'","").replace('\\', '')
                    BPLID = line['BPLID']
                    BPLName = str(line['BPLName']).replace("'","").replace('\\', '')

                    AccountName = ""
                    mycursor.execute(f"SELECT * FROM `Company_glaccounts` WHERE `Code` = '{AccountCode}'")
                    jeData = mycursor.fetchall()
                    if len(jeData) > 0:
                        AccountName = jeData[0]['Name']
                    else:
                        mycursor.execute(f"select `id`, `CardCode`, `CardName` from `BusinessPartner_businesspartner` WHERE `CardCode` = '{AccountCode}'")
                        bpData = mycursor.fetchall()
                        if len(bpData) > 0:
                            AccountName = bpData[0]['CardName']

                    line_sql = f"UPDATE `JournalEntries_journalentrylines` SET `AccountCode` = '{AccountCode}',`Debit` = '{Debit}',`Credit` = '{Credit}',`DueDate` = '{DueDate}',`ShortName` = '{ShortName}',`ContraAccount` = '{ContraAccount}',`LineMemo` = '{LineMemo}',`ReferenceDate1` = '{ReferenceDate1}',`Reference1` = '{Reference1}',`Reference2` = '{Reference2}',`BPLID` = '{BPLID}',`BPLName` = '{BPLName}',`AccountName` = '{AccountName}' WHERE `JournalEntriesId` = {JournalEntriesId} AND `Line_ID` = {Line_ID}"

                    # print(line_sql)
                    mycursor.execute(line_sql)
                    mydb.commit()

        # end for

        if 'odata.nextLink' in opts:
            nextLink = opts['odata.nextLink']
            # print(">>>>>>>>>>>>>>>>>>>>> nextLink: ", nextLink)
            nextLink = nextLink.split("skip=")
            # print(nextLink)
            skip = str(nextLink[1]).strip()

        else:
            # print("<<<<<<<<<<<<<<<<<<<<< nextLink: ", "")
            skip = ""
            exit()

        print("skip", skip)
        # end try except
    # end while
# end if

