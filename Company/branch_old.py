import requests, json
import time
import math
import mysql.connector

import sys, os

# file_path = os.path.realpath(__file__)
# file_path = str("/home/www/b2b/shivtara_live/bridge/Item/")
file_path = str("/home/www/b2b/ledure_pre/bridge/Item/")
print(">>>>>>>>>>>>>>>>>>>>>>>>>")
print("file_path: ", file_path)
dir = file_path.split("bridge")[0]+"bridge"
print("file_dir: ", dir)
print(">>>>>>>>>>>>>>>>>>>>>>>>>")
sys.path.append(dir)
from bridge import settings
ses = ""
if __name__ == '__main__':
	ses = settings.SAPSESSIONNEW("core")
	# print("in if")
else:
	ses = settings.SAPSESSIONNEW("api")
	# print("else")


mydb = mysql.connector.connect(
  host=settings.DATABASES['default']['HOST'],
  user=settings.DATABASES['default']['USER'],
  password=settings.DATABASES['default']['PASSWORD'],
  database=settings.DATABASES['default']['NAME']
)

mycursor = mydb.cursor()

# ttl = requests.get(settings.SAPURL+'/SalesPersons/$count', cookies=ses.cookies, verify=False)
sapData = requests.get(settings.SAPURL+'/BusinessPlaces/$count', cookies=ses.cookies, verify=False)

print("sapData ",sapData.text)
# count the number if loop run, each one skip 20 values
count = math.ceil(int(sapData.text)/20)
print(count)

skip=0
for i in range(count):
        
    res = requests.get(settings.SAPURL+'/BusinessPlaces?$skip='+str(skip), cookies=ses.cookies, verify=False)
    data = json.loads(res.text)
    # branches = data['value']
    for branche in data['value']:
        print('-----Branches---')
        # print(branche)
        # print(branche['BPLNameForeign'])

        BPLId = branche['BPLID']
        BPLName = str(branche['BPLName']).replace("'", "&sbquo;")
        Address = str(branche['Address']).replace("'", "&sbquo;")
        MainBPL = branche['MainBPL']
        Disabled = branche['Disabled']
        UserSign2 = ""
        UpdateDate = ""
        DflWhs = ""#branche['DflWhs']
        TaxIdNum = ""#branche['TaxIdNum']
        StreetNo = str(branche['StreetNo']).replace("'", "&sbquo;")
        Building = str(branche['Building'])
        ZipCode = str(branche['ZipCode'])
        City = str(branche['City']).replace("'", "&sbquo;")
        State = str(branche['State'])
        Country = str(branche['Country'])

        pay_sql = f"INSERT INTO `Company_branch`(`BPLId`, `BPLName`, `Address`, `MainBPL`, `Disabled`, `UserSign2`, `UpdateDate`, `DflWhs`, `TaxIdNum`, `StreetNo`, `Building`, `ZipCode`, `City`, `State`, `Country`) VALUES ('{BPLId}','{BPLName}','{Address}','{MainBPL}','{Disabled}','{UserSign2}','{UpdateDate}','{DflWhs}','{TaxIdNum}','{StreetNo}','{Building}','{ZipCode}','{City}','{State}','{Country}')"

        print(pay_sql)
        mycursor.execute(pay_sql)
        mydb.commit()
        indid = mycursor.lastrowid
        print(indid)

    print('___')
    skip = skip+20
    print(skip)
