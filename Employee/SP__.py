import requests, json
import time
import math
import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    # password='root',
    password='PUb4*#287#@5#@',
    # password='$Bridge@2022#',
    database='ledure_pre'
)
mycursor = mydb.cursor(buffered=True)

print("<><><><><><><><><><><>><><><><><><")
print("===== Login SAP ====")
data = { "CompanyDB": "LEDURE_LIVE_300323", "Password": "L!l@364%$", "UserName": "uneecloud\\led.manager", "SessionId": "7c85460c-c15a-11ed-8000-005056a40bab", "at": "2023-03-13 10:19:30", "sapurl": "https://analytics103u.uneecloud.com:50000/b1s/v1" }
r = requests.post(data['sapurl']+'/Login', data=json.dumps(data), verify=False)
print(r)

# currentDate = '2023-02-10'
serSPCount = requests.get(data['sapurl']+'/SalesPersons/$count', cookies=r.cookies, verify=False).text

# count the number if loop run, each one skip 20 values
count = math.ceil(int(serSPCount)/20)
print(count)

employeearr = []
skip=0
for t in range(count):

	res = requests.get(data['sapurl']+'/SalesPersons?$skip='+str(skip), cookies=r.cookies, verify=False)

	sps = json.loads(res.text)
	for sp in sps['value']:
		
		print('-----SalePersons---')
		# print(sp)
		EmployeeID = ""
		SalesEmpCode = sp['SalesEmployeeCode']
		employeearr.append(SalesEmpCode)

		companyID = ""
		SalesEmployeeCode = sp['SalesEmployeeCode']
		if str(SalesEmployeeCode) == '-1':
			continue

		SalesEmployeeName = sp['SalesEmployeeName']
		EmployeeID = sp['EmployeeID']
		userName = sp['SalesEmployeeName']
		password = "123"
		firstName = sp['SalesEmployeeName']
		middleName = ""
		lastName = ""
		Email = sp['Email']
		Mobile = sp['Mobile']
		role = ""
		position = ""
		branch = ""
		Active = sp['Active']
		passwordUpdatedOn = ""
		lastLoginOn = ""
		logedIn = ""
		reportingTo = -1
		FCM = ""
		timestamp = ""
		unit = ""
		ACCNo = ""
		Address = ""
		CompName = ""
		GST = ""
		Ifsc = ""
		U_LAT = ""
		U_LONG = ""
		Website = ""
		LocationSharing = ""
		Zone = ""
		sqlSelect = f"SELECT `id` FROM Employee_employee WHERE SalesEmployeeCode = {SalesEmpCode}"
		print(sqlSelect)
		mycursor.execute(sqlSelect)
		empObj = mycursor.fetchall()
		if len(empObj) == 0:
						
			sp_sql = f"INSERT INTO `Employee_employee`(`companyID`, `SalesEmployeeCode`, `SalesEmployeeName`, `EmployeeID`, `userName`, `password`, `firstName`, `middleName`, `lastName`, `Email`, `Mobile`, `role`, `position`, `branch`, `Active`, `passwordUpdatedOn`, `lastLoginOn`, `logedIn`, `reportingTo`, `FCM`, `timestamp`, `unit`, `ACCNo`, `Address`, `CompName`, `GST`, `Ifsc`, `U_LAT`, `U_LONG`, `Website`, `LocationSharing`, `Zone`) VALUES ('{companyID}','{SalesEmployeeCode}','{SalesEmployeeName}','{EmployeeID}','{userName}','{password}','{firstName}','{middleName}','{lastName}','{Email}','{Mobile}','{role}','{position}','{branch}','{Active}','{passwordUpdatedOn}','{lastLoginOn}','{logedIn}','{reportingTo}','{FCM}','{timestamp}','{unit}','{ACCNo}','{Address}','{CompName}','{GST}','{Ifsc}','{U_LAT}','{U_LONG}','{Website}','{LocationSharing}','{Zone}');"
			print(sp_sql)
			mycursor.execute(sp_sql)
			mydb.commit()
			spid = mycursor.lastrowid
			print(spid)
		else:
			sp_sql = f"UPDATE `Employee_employee` SET `SalesEmployeeName`='{SalesEmployeeName}',`EmployeeID` = '{EmployeeID}',`userName`='{SalesEmployeeName}',`firstName`='{SalesEmployeeName}', `Email`='{Email}',`Mobile`='{Mobile}',`Active`='{Active}' WHERE SalesEmployeeCode = {SalesEmployeeCode}"
			print(sp_sql)
			mycursor.execute(sp_sql)
			mydb.commit()
			# spid = mycursor.lastrowid
			# print(spid)


	print('___')
	skip = skip+20
	print(skip)