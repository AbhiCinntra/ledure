import requests, json
import time
import math
import mysql.connector

import sys, os

# file_path = os.path.dirname(__file__)
# file_path = str("/home/www/b2b/ledure_pre/bridge/Item/")
file_path = str("/home/www/b2b/ledure_dev/bridge/Item/")
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
# mycursor = mydb.cursor()
mycursor = mydb.cursor(dictionary=True, buffered=True)

# res = requests.get(data['sapurl']+'/Items/$count', headers={'Authorization': "Bearer "+data['SessionId']+""}, verify=False)
res = requests.get(settings.SAPURL+'/Items/$count', cookies=ses.cookies, verify=False)
# print(res.text)

pages = math.ceil(int(res.text)/20)
# print(pages)
skip=0
for page in range(pages):

    # res = requests.get(data['sapurl']+"/Items?$skip="+str(skip), headers={'Authorization': "Bearer "+data['SessionId']+""}, verify=False)
    res = requests.get(settings.SAPURL+'/Items?$skip='+str(skip), cookies=ses.cookies, verify=False)
    items = json.loads(res.text)
    for item in items['value']:
        # print('-----Insert Item---')
        # print(item['ItemName'])
        ItemName = str(item['ItemName']).replace('"', "")
        price = str(0)
        
        # item price list by price list category
        ItemPricesList = item['ItemPrices']
        
        # warehouse list 
        ItemWarehouseInfoCollection = item['ItemWarehouseInfoCollection']
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        ActiveStatus = "tYES"
        Frozen = item['Frozen']
        if str(Frozen) == 'tYES': # Frozen tYes means item in-active
            ActiveStatus = "tNO"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        CodeType = "Manual"
        ItemName = ItemName
        ItemCode = str(item['ItemCode'])
        Inventory = str(item['QuantityOnStock'])
        Description = ItemName
        UnitPrice = ItemPricesList[0]['Price']
        Currency = "INR"
        HSN = ""
        TaxCode = ''
        Discount = "0"
        Status            = ActiveStatus
        CreatedDate       = str(item['CreateDate'])
        CreatedTime       = str(item['CreateTime'])
        UpdatedDate       = str(item['UpdateDate'])
        UpdatedTime       = str(item['UpdateTime'])
        UnitWeight        = str(item['SalesUnitWeight'])
        SalesItemsPerUnit = str(item['SalesItemsPerUnit'])
        CatID_id          = 0
        UoS               = str(item['SalesUnit'])
        Packing           = ""
        ItemsGroupCode    = str(item['ItemsGroupCode'])
        # U_GST             = str(item['U_GST'])
        U_GST             = ""
        GSTTaxCategory    = str(item['GSTTaxCategory'])
        U_UTL_ITSBG       = str(item['U_UTL_ITSBG']).replace('"', "")
        U_UTL_ITMCT       = str(item['U_UTL_ITMCT']).replace('"', "")
        U_UTL_ST_ISSERVICE = str(item['U_UTL_ST_ISSERVICE'])
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        itemSelectQuery = f"select ItemCode from Item_item where ItemCode='{item['ItemCode']}'"
        #print(itemSelectQuery)
        mycursor.execute(itemSelectQuery)
        mycursor.fetchall()
        rc = mycursor.rowcount
        #print("localItemCount", rc)
        if rc != 1:
            print(">>>>> Insert Item: ", ItemCode)
            
            selectCategory = f"SELECT `id`, `Number`, `CategoryName` FROM `Item_category` WHERE `Number` = '{ItemsGroupCode}'"
            mycursor.execute(selectCategory)
            catRow = mycursor.fetchall()
            rc = mycursor.rowcount
            if int(rc) != 0:
                #print(catRow)
                CatID_id = catRow[0]['id']

            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            ItemUnitOfMeasurementCollection = item['ItemUnitOfMeasurementCollection']
            UoMIds = []
            for uom in ItemUnitOfMeasurementCollection:
                if uom["UoMType"] == "iutPurchasing":
                    UoMIds.append(uom['UoMEntry'])
            #print("UoMIds: ", UoMIds)
            # UoMIds = ",".join(UoMIds)
            UoMIds = ",".join(str(id) for id in UoMIds)
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            item_sql = f'INSERT INTO `Item_item`(`CodeType`, `ItemName`, `ItemCode`, `Inventory`, `Description`, `UnitPrice`, `Currency`, `HSN`, `TaxCode`, `Discount`, `Status`, `CreatedDate`, `CreatedTime`, `UpdatedDate`, `UpdatedTime`, `CatID_id`, `UoS`, `UnitWeight`, `Packing`, `ItemsGroupCode`, `U_GST`,`GSTTaxCategory`, `SalesItemsPerUnit`, `UoMIds`, `U_UTL_ITSBG`, `U_UTL_ITMCT`, `U_UTL_ST_ISSERVICE`) VALUES ("{CodeType}", "{ItemName}", "{ItemCode}", "{Inventory}", "{Description}", "{UnitPrice}", "{Currency}", "{HSN}", "{TaxCode}", "{Discount}", "{Status}", "{CreatedDate}", "{CreatedTime}", "{UpdatedDate}", "{UpdatedTime}", "{CatID_id}", "{UoS}", "{UnitWeight}", "{Packing}", "{ItemsGroupCode}", "{U_GST}", "{GSTTaxCategory}", "{SalesItemsPerUnit}", "{UoMIds}", "{U_UTL_ITSBG}", "{U_UTL_ITMCT}", "{U_UTL_ST_ISSERVICE}")' 
            print(item_sql)
            mycursor.execute(item_sql)
            mydb.commit()
            
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # ItemPriceList
            #print("Insert Item Price List")
            for prices in ItemPricesList:
                lv_PriceList = prices['PriceList']
                lv_Currency = prices['Currency']
                lv_Price = prices['Price']
                item_pricelist_sql = f'INSERT INTO `Item_itempricelist`(`ItemCode`, `PriceList`, `Currency`, `Price`) VALUES ("{ItemCode}", "{lv_PriceList}", "{lv_Currency}", "{lv_Price}")'     
                #print(item_pricelist_sql)
                mycursor.execute(item_pricelist_sql)
                mydb.commit()
            
            
            for warehouse in ItemWarehouseInfoCollection:
                lv_ItemCode = warehouse['ItemCode']
                lv_WarehouseCode = warehouse['WarehouseCode']
                lv_InStock = warehouse['InStock']
                lv_StandardAveragePrice = warehouse['StandardAveragePrice']
                item_warehouse_sql = f'INSERT INTO `Item_itemwarehouse`(`ItemCode`, `WarehouseCode`, `InStock`, `StandardAveragePrice`) VALUES ("{ItemCode}", "{lv_WarehouseCode}", "{lv_InStock}", "{lv_StandardAveragePrice}")'
                #print(item_warehouse_sql)
                mycursor.execute(item_warehouse_sql)
                mydb.commit()
        else:
            print(">>>>Update Item: ", ItemCode)
            # selectCategory = f"SELECT `id`, `Number`, `CategoryName` FROM `Item_category` WHERE `Number` = '{ItemsGroupCode}'"
            # mycursor.execute(selectCategory)
            # catRow = mycursor.fetchall()
            # rc = mycursor.rowcount
            # if int(rc) != 0:
            #     #print(catRow)
            #     CatID_id = catRow[0]['id']
            
            # # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # ItemUnitOfMeasurementCollection = item['ItemUnitOfMeasurementCollection']
            # UoMIds = []
            # for uom in ItemUnitOfMeasurementCollection:
            #     if uom["UoMType"] == "iutPurchasing":
            #         UoMIds.append(uom['UoMEntry'])
            # # UoMIds = ",".join(UoMIds)
            # UoMIds = ",".join(str(id) for id in UoMIds)
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # item_sql = f'UPDATE `Item_item` SET `ItemName`="{ItemName}",`Inventory`="{Inventory}", `Status`="{Status}", `CreatedDate` = "{CreatedDate}", `CreatedTime`="{CreatedTime}", `UpdatedDate`="{UpdatedDate}",`UpdatedTime`="{UpdatedTime}",`UoS`="{UoS}", `U_GST`="{U_GST}", `UnitWeight`="{UnitWeight}", `GSTTaxCategory` = "{GSTTaxCategory}", `SalesItemsPerUnit` = "{SalesItemsPerUnit}", `UoMIds` = "{UoMIds}", `UnitPrice` = "{UnitPrice}", `CatID_id` = "{CatID_id}", `U_UTL_ITSBG` = "{U_UTL_ITSBG}",`U_UTL_ITMCT` = "{U_UTL_ITMCT}",`U_UTL_ST_ISSERVICE` = "{U_UTL_ST_ISSERVICE}" WHERE `ItemCode` = "{ItemCode}"'
            item_sql = f'UPDATE `Item_item` SET `ItemName`="{ItemName}",`Inventory`="{Inventory}", `Status`="{Status}", `CreatedDate` = "{CreatedDate}", `CreatedTime`="{CreatedTime}", `UpdatedDate`="{UpdatedDate}",`UpdatedTime`="{UpdatedTime}",`UoS`="{UoS}", `U_GST`="{U_GST}", `UnitWeight`="{UnitWeight}", `GSTTaxCategory` = "{GSTTaxCategory}", `SalesItemsPerUnit` = "{SalesItemsPerUnit}", `UnitPrice` = "{UnitPrice}", `U_UTL_ITSBG` = "{U_UTL_ITSBG}",`U_UTL_ITMCT` = "{U_UTL_ITMCT}",`U_UTL_ST_ISSERVICE` = "{U_UTL_ST_ISSERVICE}" WHERE `ItemCode` = "{ItemCode}"'
            print(item_sql)
            mycursor.execute(item_sql)
            mydb.commit()
            
            continue
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # ItemPriceList
            #print("Insert Item Price List")
            for prices in ItemPricesList:
                lv_PriceList = prices['PriceList']
                lv_Currency = prices['Currency']
                lv_Price = prices['Price']
                item_pricelist_sql = f'UPDATE `Item_itempricelist` SET `Currency`="{lv_Currency}",`Price`="{lv_Price}" WHERE `ItemCode` = "{ItemCode}" AND `PriceList` = "{lv_PriceList}"'    
                #print(item_pricelist_sql)
                mycursor.execute(item_pricelist_sql)
                mydb.commit()

            for warehouse in ItemWarehouseInfoCollection:
                lv_WarehouseCode = warehouse['WarehouseCode']
                lv_ItemCode = warehouse['ItemCode']
                lv_InStock = warehouse['InStock']
                lv_StandardAveragePrice = warehouse['StandardAveragePrice']
                
                warehouseSelectQuery = f"SELECT * FROM `Item_itemwarehouse` WHERE `ItemCode` = '{ItemCode}' AND WarehouseCode='{lv_WarehouseCode}'"
                mycursor.execute(warehouseSelectQuery)
                rc = mycursor.rowcount
                item_warehouse_sql = ""
                if rc != 1:
                    item_warehouse_sql = f'INSERT INTO `Item_itemwarehouse`(`ItemCode`, `WarehouseCode`, `InStock`, `StandardAveragePrice`) VALUES ("{ItemCode}", "{lv_WarehouseCode}", "{lv_InStock}", "{lv_StandardAveragePrice}")'
                else:
                    item_warehouse_sql = f'UPDATE `Item_itemwarehouse` SET `ItemCode` = "{ItemCode}",`InStock` = "{lv_InStock}",`StandardAveragePrice` = "{lv_StandardAveragePrice}" WHERE `WarehouseCode` = "{lv_WarehouseCode}"'
                
                print(item_warehouse_sql)
                mycursor.execute(item_warehouse_sql)
                mydb.commit()
        
    #print('___')
    skip = skip+20
