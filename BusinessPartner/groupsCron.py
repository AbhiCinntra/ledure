import requests, json
import time
import math
import mysql.connector
import sys, os

# file_path = os.path.dirname(__file__)
# file_path = str("F:/python-projects/shivtara_live/bridge/Item/")
file_path = str("/home/www/b2b/ledure_pre/bridge/")
print(">>>>>>>>>>>>>>>>>>>>>>>>>")
print("file_path: ", file_path)
dir = file_path.split("bridge")[0]+"bridge"
sys.path.append(dir)
from bridge import settings
ses = ""
if __name__ == '__main__':
	ses = settings.SAPSESSIONNEW("core")
else:
	ses = settings.SAPSESSIONNEW("api")

mydb = mysql.connector.connect(
  host=settings.DATABASES['default']['HOST'],
  user=settings.DATABASES['default']['USER'],
  password=settings.DATABASES['default']['PASSWORD'],
  database=settings.DATABASES['default']['NAME']
)

mycursor = mydb.cursor()

sapData = requests.get(settings.SAPURL+'/BusinessPartnerGroups/$count', cookies=ses.cookies, verify=False)
print("sapData ", sapData.text)

# count the number if loop run, each one skip 20 values
count = math.ceil(int(sapData.text)/20)
print(count)
skip=0
for i in range(count):
  res = requests.get(settings.SAPURL+'/BusinessPartnerGroups?$skip='+str(skip), cookies=ses.cookies, verify=False)
  inds = json.loads(res.text)
    
  for ind in inds['value']:
    print('-----Payment-----')
    GroupNumber = ind['Code']
    GroupName = ind['Name']

    mycursor.execute("select * from `BusinessPartner_businesspartnergroups` WHERE Code='"+str(GroupNumber)+"'")
    mycursor.fetchall()
    rc = mycursor.rowcount
    if rc != 1:
      pay_sql = f"INSERT INTO `BusinessPartner_businesspartnergroups`(`Code`, `Name`) VALUES ('{GroupNumber}','{GroupName}');"
      print(pay_sql)
      mycursor.execute(pay_sql)
      mydb.commit()
      
    else:
      ind_sql = f"UPDATE `BusinessPartner_businesspartnergroups` SET `Name`='{GroupName}' WHERE `Code` = {GroupNumber}"
      print(ind_sql)
      mycursor.execute(ind_sql)
      mydb.commit()