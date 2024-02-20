import requests, json
import time
import math
import mysql.connector

import sys, os
# dir = os.getcwd()
# dir = dir.split("bridge")[0]+"bridge"
# sys.path.append(dir)
# from bridge import settings
# data = settings.SAPSESSION("core")

# file_path = os.path.dirname(__file__)
# file_path = str("F:/python-projects/ledure_pre/bridge/Item/")
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

mycursor = mydb.cursor(dictionary=True, buffered=True)
# exit()
# res = requests.get(data['sapurl']+'/ItemGroups/$count', headers={'Authorization': "Bearer "+data['SessionId']+""}, verify=False)
res = requests.get(settings.SAPURL+'/ItemGroups/$count', cookies=ses.cookies, verify=False)
print(res.text)

pages = math.ceil(int(res.text)/20)
print(pages)

skip=0

for page in range(pages):
	# res = requests.get(data['sapurl']+"/ItemGroups?$select=Number,GroupName&$orderby=Number&$skip="+str(skip), headers={'Authorization': "Bearer "+data['SessionId']+""}, verify=False)
	res = requests.get(settings.SAPURL+'/ItemGroups?$select=Number,GroupName&$orderby=Number&$skip='+str(skip), cookies=ses.cookies, verify=False)
	cats = json.loads(res.text)

	for cat in cats['value']:
		print('-----Category---')
		print(cat['Number'])
		GroupName = cat['GroupName'].replace("'", "''")
		print(GroupName)
		mycursor.execute("select * from Item_category where Number='"+str(cat['Number'])+"'")
		mycursor.fetchall()
		rc = mycursor.rowcount
		print(rc)
		if rc != 1:
			cat_sql = f"INSERT INTO `Item_category`(`CategoryName`, `Status`, `CreatedDate`, `CreatedTime`, `UpdatedDate`, `UpdatedTime`, `Number`) VALUES ('{GroupName}', 1, '','','','', '{cat['Number']}')"
			print(cat_sql)
			mycursor.execute(cat_sql)
			mydb.commit()
			catid = mycursor.lastrowid
			print(catid)
		else:
			cat_sql = f"UPDATE `Item_category` SET `CategoryName`='{GroupName}' WHERE `Number`={str(cat['Number'])}"
			print(cat_sql)
			mycursor.execute(cat_sql)
			mydb.commit()

	print('___')
	skip = skip+20
