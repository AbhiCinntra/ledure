import math
from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse

from Pagination.models import Pagination
from Invoice.models import IncomingPaymentInvoices, Invoice
from BusinessPartner.models import BusinessPartner, BusinessPartnerGroups
from Order.models import Order, DocumentLines as Order_DocumentLines
from BusinessPartner.models import BPBranch
from PaymentTermsTypes.models import PaymentTermsTypes
from global_methods import *
from .models import *
from Employee.models import Employee
import mysql.connector

# import invoice
from Invoice.models import DocumentLines as Invoice_DocumentLines
from DeliveryNote.models import DocumentLines as Delivery_DocumentLines
import requests, json

from rest_framework.decorators import api_view  
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import *
from rest_framework.parsers import JSONParser

from pytz import timezone
from datetime import datetime as dt

# import setting file
from django.conf import settings
from django.db.models import Q
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
date = dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d')
yearmonth = dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m')
time = dt.now(timezone("Asia/Kolkata")).strftime('%H:%M %p')
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#Item Create API
@api_view(['POST'])
def create(request):
    if request.data['CodeType']=='Manual':
        if Item.objects.filter(ItemCode=request.data['ItemCode']).exists():
            return Response({"message":"Already exist ItemCode","status":"409","data":[]})
        elif request.data['TaxCode'] >= 1 or request.data['Discount'] >= 1:
            return Response({"message":"TaxCode and Discount should be less than 1","status":"409","data":[]})
        else:
            try:        
                CodeType = request.data['CodeType']
                ItemName = request.data['ItemName']
                ItemCode = request.data['ItemCode']
                CatID = request.data['CatID']
                Inventory = request.data['Inventory']
                Description = request.data['Description']
                UnitPrice = request.data['UnitPrice']
                UoS = request.data['UoS']
                Packing = request.data['Packing']
                Currency = request.data['Currency']
                HSN = request.data['HSN']
                TaxCode = request.data['TaxCode']
                Discount = request.data['Discount']
                Status = request.data['Status']
                CreatedDate = request.data['CreatedDate']
                CreatedTime = request.data['CreatedTime']
                UpdatedDate = request.data['UpdatedDate']
                UpdatedTime = request.data['UpdatedTime']
                
                CatID = Category.objects.get(pk=CatID)

                model = Item(CodeType = CodeType, ItemName = ItemName, ItemCode = ItemCode, CatID = CatID, Inventory=Inventory, Description = Description, UnitPrice = UnitPrice, UoS = UoS, Packing=Packing, Currency = Currency, HSN = HSN, TaxCode = TaxCode, Discount = Discount, Status = Status, CreatedDate = CreatedDate, CreatedTime = CreatedTime, UpdatedDate = UpdatedDate, UpdatedTime = UpdatedTime)
                model.save()
                prod = Item.objects.latest('id')        
                return Response({"message":"successful","status":200,"data":[{"id":prod.id}]})
            except Exception as e:
                return Response({"message":"Not Created","status":201,"data":[{"Error":str(e)}]})
    
    elif request.data['CodeType']=='Series':
        if request.data['TaxCode'] >= 1 or request.data['Discount'] >= 1:
            return Response({"message":"TaxCode and Discount should be less than 1","status":"409","data":[]})
        else:
            try:
                CodeType = request.data['CodeType']
                ItemName = request.data['ItemName']
                #ItemCode = request.data['ItemCode']
                CatID = request.data['CatID']
                Inventory = request.data['Inventory']
                Description = request.data['Description']
                UnitPrice = request.data['UnitPrice']
                UoS = request.data['UoS']
                Packing = request.data['Packing']
                Currency = request.data['Currency']
                HSN = request.data['HSN']
                TaxCode = request.data['TaxCode']
                Discount = request.data['Discount']
                Status = request.data['Status']
                CreatedDate = request.data['CreatedDate']
                CreatedTime = request.data['CreatedTime']
                UpdatedDate = request.data['UpdatedDate']
                UpdatedTime = request.data['UpdatedTime']
                
                CatID = Category.objects.get(pk=CatID)

                model = Item(CodeType = CodeType, ItemName = ItemName, CatID = CatID, Inventory=Inventory, Description = Description, UnitPrice = UnitPrice, UoS = UoS, Packing=Packing, Currency = Currency, HSN = HSN, TaxCode = TaxCode, Discount = Discount, Status = Status, CreatedDate = CreatedDate, CreatedTime = CreatedTime, UpdatedDate = UpdatedDate, UpdatedTime = UpdatedTime)
                model.save()
                prod = Item.objects.latest('id')        
                pid = format(prod.id, '06')                
                model.ItemCode = "IT"+str(pid)
                model.save()
                
                return Response({"message":"successful","status":200,"data":[{"id":prod.id}]})
            except Exception as e:
                return Response({"message":"Not Created","status":201,"data":[{"Error":str(e)}]})

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#Item Create API R&D
@api_view(['POST'])
def create_test(request):
    try:
        # model = makemodel(request)
        print("Item("+str(model)+")")
        ss = "Item("+str(model)+")"
        model = Item(ss)
        print(model)
        model.save()
        
        return Response({"message":"successful","status":200,"data":[]})
    except Exception as e:
        return Response({"message":"Not Created","status":201,"data":[{"Error":str(e)}]})

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#Item Update API
@api_view(['POST'])
def update(request):
    fetchid = request.data['id']
    if request.data['TaxCode'] >= 1 or request.data['Discount'] >= 1:
        return Response({"message":"TaxCode and Discount should be less than 1","status":"409","data":[]})
    else:
        try:
            model = Item.objects.get(pk = fetchid)
            model.ItemName = request.data['ItemName']
            CatID = Category.objects.get(pk=request.data['CatID'])
            model.CatID = CatID
            model.Inventory = request.data['Inventory']
            model.Description = request.data['Description']
            model.UnitPrice = request.data['UnitPrice']
            model.UoS = request.data['UoS']
            model.Packing = request.data['Packing']
            model.Currency = request.data['Currency']
            model.HSN = request.data['HSN']
            model.TaxCode = request.data['TaxCode']
            model.Discount = request.data['Discount']
            model.Status = request.data['Status']
            model.UpdatedDate = request.data['UpdatedDate']
            model.UpdatedTime = request.data['UpdatedTime']            
            model.save()
            return Response({"message":"successful","status":200, "data":[request.data]})
        except Exception as e:
            return Response({"message":"Not Update","status":201,"data":[{"Error":str(e)}]})

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#Item All API
@api_view(["POST"])
def all(request):
    try:
        PriceListId = request.data['PriceListId']
        if "CatID" in request.data:
            Items_obj = Item.objects.filter(CatID=request.data['CatID'], Status = 'tYES').order_by("-id")
            # prod_json = ItemSerializer(Items_obj, many=True)
            # return Response({"message": "Success","status": 200,"data":prod_json.data})
            result = showItems(Items_obj, PriceListId)
            return Response({"message": "Success","status": 200,"data":result})
        else:
            Items_obj = Item.objects.filter(Status = 'tYES').order_by("-id")
            # prod_json = ItemSerializer(Items_obj, many=True)
            # return Response({"message": "Success","status": 200,"data":prod_json.data})
            result = showItems(Items_obj, PriceListId)
            return Response({"message": "Success","status": 200,"data":result})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#Item One API
@api_view(["POST"])
def one(request):
    id=request.data['id'] 
    PriceListId = request.data['PriceListId']   
    Items_obj = Item.objects.filter(id=id)
    # prod_json = ItemSerializer(Items_obj, many=False)
    # return Response({"message": "Success","status": 200,"data":[prod_json.data]})
    result = showItems(Items_obj, PriceListId)
    return Response({"message": "Success","status": 200,"data":result})

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#Item delete
@api_view(['POST'])
def delete(request):
    fetchid=request.data['id']
    try:
        fetchdata=Item.objects.filter(pk=fetchid).delete()
        return Response({"message":"successful","status":"200","data":[]})        
    except:
         return Response({"message":"Id wrong","status":"201","data":[]})

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#Item Create API
@api_view(['POST'])
def tax_create(request):
    if request.data['TaxCode'] >= 1:
        return Response({"message":"TaxCode should be less than 1", "status":"201","data":[]})
    elif Tax.objects.filter(TaxCode=request.data['TaxCode']).exists():
        return Response({"message":"Already exist TaxCode","status":"409","data":[]})
    elif Tax.objects.filter(TaxName=request.data['TaxName']).exists():
        return Response({"message":"Already exist TaxName","status":"409","data":[]})
    else:
        try:        
            TaxName = request.data['TaxName']
            TaxCode = request.data['TaxCode']
            CreatedDate = request.data['CreatedDate']
            CreatedTime = request.data['CreatedTime']

            model = Tax(TaxName = TaxName, TaxCode = TaxCode, CreatedDate = CreatedDate, CreatedTime = CreatedTime)
            model.save()
            tax = Tax.objects.latest('id')        
            return Response({"message":"successful","status":200,"data":[{"id":tax.id}]})
        except Exception as e:
            return Response({"message":"Not Created","status":201,"data":[{"Error":str(e)}]})

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#Tax All API
@api_view(["GET"])
def tax_all(request):
    tax_obj = Tax.objects.all().order_by("-id")
    tax_json = TaxSerializer(tax_obj, many=True)
    return Response({"message": "Success","status": 200,"data":tax_json.data})

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#Tax Update API
@api_view(['POST'])
def tax_update(request):
    fetchid = request.data['id']
    if request.data['TaxCode'] >= 1:
        return Response({"message":"TaxCode should be less than 1", "status":"201","data":[]})
    else:
        try:
            model = Tax.objects.get(pk = fetchid)
            model.TaxName = request.data['TaxName']
            model.TaxCode = request.data['TaxCode']
            model.save()
            return Response({"message":"successful","status":200, "data":[request.data]})
        except Exception as e:
            return Response({"message":"Not Update","status":201,"data":[{"Error":str(e)}]})

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#Tax One API
@api_view(["POST"])
def tax_one(request):
    id=request.data['id']    
    tax_obj = Tax.objects.get(id=id)
    tax_json = TaxSerializer(tax_obj, many=False)
    return Response({"message": "Success","status": 200,"data":[tax_json.data]})

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#Category Create API
@api_view(['POST'])
def category_create(request):
    if Category.objects.filter(CategoryName=request.data['CategoryName']).exists():
        return Response({"message":"Already exist CategoryName","status":"409","data":[]})
    else:
        try:        
            CategoryName = request.data['CategoryName']
            Status = request.data['Status']
            CreatedDate = request.data['CreatedDate']
            CreatedTime = request.data['CreatedTime']
            UpdatedDate = request.data['UpdatedDate']
            UpdatedTime = request.data['UpdatedTime']

            model = Category(CategoryName = CategoryName, Status = Status, CreatedDate = CreatedDate, CreatedTime = CreatedTime, UpdatedDate=CreatedDate, UpdatedTime=CreatedTime)
            model.save()
            category = Category.objects.latest('id')        
            return Response({"message":"successful","status":200,"data":[{"id":category.id}]})
        except Exception as e:
            return Response({"message":"Not Created","status":201,"data":[{"Error":str(e)}]})

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#Category All API
@api_view(["GET"])
def category_all(request):
    category_obj = Category.objects.filter(Status = 1).order_by("-id")
    category_json = CategorySerializer(category_obj, many=True)
    return Response({"message": "Success","status": 200,"data":category_json.data})

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#Category Update API
@api_view(['POST'])
def category_update(request):
    fetchid = request.data['id']
    if Category.objects.filter(CategoryName=request.data['CategoryName']).exists():
        return Response({"message":"Already exist CategoryName","status":"409","data":[]})
    else:
        try:
            model = Category.objects.get(pk = fetchid)
            model.CategoryName = request.data['CategoryName']
            model.Status = request.data['Status']
            model.UpdatedDate = request.data['UpdatedDate']
            model.UpdatedTime = request.data['UpdatedTime']
            model.save()
            return Response({"message":"successful","status":200, "data":[request.data]})
        except Exception as e:
            return Response({"message":"Not Update","status":201,"data":[{"Error":str(e)}]})

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#Category One API
@api_view(["POST"])
def category_one(request):
    id=request.data['id']    
    category_obj = Category.objects.get(id=id)
    category_json = CategorySerializer(category_obj, many=False)
    return Response({"message": "Success","status": 200,"data":[category_json.data]})

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#All Uom List
@api_view(["GET"])
def all_uom(request):
    try:
        UoMList_obj = UoMList.objects.all()
        UoMList_json = UoMListSerializer(UoMList_obj, many=True)
        return Response({"message": "Success","status": 200,"data":UoMList_json.data})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(["POST"])
def all_filter_uom(request):
    try:
        UoMIds = (request.data['UoMIds']).split(",")
        UoMList_obj = UoMList.objects.filter(AbsEntry__in = UoMIds)
        UoMList_json = UoMListSerializer(UoMList_obj, many=True)
        return Response({"message": "Success","status": 200,"data":UoMList_json.data})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# update Category
@api_view(['GET'])
def itemcategoryupdate(request):
    # try:
    if True:
        catCount = (settings.CALLAPI('get', f"/ItemGroups/$count", 'api', '')).text
        pages = math.ceil(int(catCount)/20)
        print("pages: ",pages)
        skip=0
        for page in range(pages):
            res = settings.CALLAPI('get', f"/ItemGroups?$select=Number,GroupName&$orderby=Number&$skip={skip}", 'api', '')
            resData = json.loads(res.text)
            if 'odata.metadata' in resData:
                cats = resData['value']
                for cat in cats:
                    # print("ItemGroup :", cat)
                    Number = int(cat['Number'])
                    GroupName = cat['GroupName']
                    if Category.objects.filter(Number = Number).exists():
                        Category.objects.filter(Number = Number).update(CategoryName = GroupName)
                    else:
                        print('insert')
                        Category(Number = Number, CategoryName = GroupName, Status = 1).save()
            else:
                SAP_MSG = resData['error']['message']['value']
                return Response({"message":SAP_MSG,"SAP_error":SAP_MSG, "status":202,"data":[]})
            skip = skip+20
        return Response({"message":"Successful","status":200, "data":[]})
    # except Exception as e:
    #     return Response({"message":str(e),"status":201,"Model": "BP" ,"data":[]})

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# update Category Items and Uom
@api_view(['GET'])
def syncInventroy(request):
    try:
        # Import and sync item category
        itemCat ="Item/import-category.py"
        exec(compile(open(itemCat, "rb").read(), itemCat, 'exec'), {})
        
        # Import and sync items price list
        itemPriceList ="Item/import-priceList.py"
        exec(compile(open(itemPriceList, "rb").read(), itemPriceList, 'exec'), {})
       
        # Import and sync items price list
        itemUom ="Item/import-uom.py"
        exec(compile(open(itemUom, "rb").read(), itemUom, 'exec'), {})
        
        # Import and sync items
        itemData ="Item/import-item.py"
        exec(compile(open(itemData, "rb").read(), itemData, 'exec'), {})

        # Import and Update items
        # itemUpdate ="Item/update-imported-item.py"
        # exec(compile(open(itemPriceList, "rb").read(), itemUpdate, 'exec'), {})

        return Response({"message":"Successful","status":200, "data":[]})
    except Exception as e:
        return Response({"message":str(e),"status":201,"Model": "Items" ,"data":[]})

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(['POST'])
def searchInItems(request):
    try:
        SearchText = request.data['SearchText']
        PageNo = request.data['PageNo']
        PriceListId = request.data['PriceListId']
        WarehouseCode = request.data['WarehouseCode']
        MaxItem = 50
        endWith = (PageNo * MaxItem)
        startWith = (endWith - MaxItem)

        itemsObj = ""
        item_count = 0
        if 'ItemsGroupCode' in request.data:
            ItemsGroupCode = request.data['ItemsGroupCode']
            itemsObj = Item.objects.filter(
                Q(ItemsGroupCode = ItemsGroupCode) &
                Q(
                    Q(ItemCode__icontains = SearchText) |
                    Q(ItemName__icontains = SearchText)
                )
            ).order_by('-id')[startWith:endWith]

            item_count = Item.objects.filter(ItemsGroupCode_id = ItemsGroupCode).count()

        else:
            itemsObj = Item.objects.filter(
                Q(ItemCode__icontains = SearchText) |
                Q(ItemName__icontains = SearchText)
            ).order_by('-id')[startWith:endWith]

            item_count = Item.objects.filter( Q(ItemCode__icontains = SearchText) | Q(ItemName__icontains = SearchText) ).count()
            
        # itemsJson = ItemSerializer(itemsObj, many=True)
        itemData = showItems(itemsObj, PriceListId, WarehouseCode)
        
        return Response({"message": "Success","status": 200, "count": item_count, "data":itemData})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(["POST"])
def all_filter_pagination(request):
    try:
        PriceListId = request.data['PriceListId']
        WarehouseCode = request.data['WarehouseCode']
        PageNo = int(request.data['PageNo'])
        MaxSize = int(request.data['MaxSize'])
        ItemCount = 0
        if MaxSize != "All":
            size = int(MaxSize)
            endWith = (PageNo * size)
            startWith = (endWith - size)
            print("in not all pricelist")

            print("startWith:endWith ", startWith, ":", endWith)
            if "CatID" in request.data:
                ItemCount = Item.objects.filter(CatID=request.data['CatID'], Status = 'tYES').count()
                Items_obj = Item.objects.filter(CatID=request.data['CatID'], Status = 'tYES').order_by("-id")[startWith:endWith]
            else:
                ItemCount = Item.objects.filter(Status = 'tYES').count()
                Items_obj = Item.objects.filter(Status = 'tYES').order_by("-id")[startWith:endWith]
        else:
            print("in all pricelist")
            if "CatID" in request.data:
                ItemCount = Item.objects.filter(CatID=request.data['CatID'], Status = 'tYES').count()
                Items_obj = Item.objects.filter(CatID=request.data['CatID'], Status = 'tYES').order_by("-id")
            else:
                ItemCount = Item.objects.filter(Status = 'tYES').count()
                Items_obj = Item.objects.filter(Status = 'tYES').order_by("-id")
        result = showItems(Items_obj, PriceListId, WarehouseCode)
        return Response({"message": "Success", "status": 200, "data":result, "ItemCount": ItemCount})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def showItems(objs, PriceListId = 1, WarehouseCode = ""):
    allItems = []
    for obj in objs:
        item_json = ItemSerializer(obj, many=False)
        finalItem = json.loads(json.dumps(item_json.data))

        # get price by price list
        if ItemPriceList.objects.filter(ItemCode = obj.ItemCode, PriceList = PriceListId).exists():
            itemPriceObj = ItemPriceList.objects.filter(ItemCode = obj.ItemCode, PriceList = PriceListId)[0]
            finalItem['UnitPrice'] = itemPriceObj.Price
        
        # get stock in warehouse
        if ItemWarehouse.objects.filter(ItemCode = obj.ItemCode, WarehouseCode = WarehouseCode):
            objWarehouse = ItemWarehouse.objects.filter(ItemCode = obj.ItemCode, WarehouseCode = WarehouseCode).first()
            finalItem['InStock'] = str(objWarehouse.InStock)
        else:
            finalItem['InStock'] = 0

        allItems.append(finalItem)
    return allItems
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
from django.db import connection as db_connection
@api_view(['POST'])
def filter_item_dashboard(request):
    try:
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # Filter = request.data['Filter']
        # SalesType = request.data['Type']
        FromDate = request.data['FromDate']
        ToDate = request.data['ToDate']
        SearchText = request.data['SearchText']
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        SalesPersonCode = -1
        if 'SalesPersonCode' in request.data:
            SalesPersonCode = request.data['SalesPersonCode']
        zones = getZoneByEmployee(SalesPersonCode)
        zonesStr = "','".join(zones)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        if str(SearchText).strip() != "":
            categoryObjs = Category.objects.filter(Q(CategoryName__icontains = SearchText))
        else:
            categoryObjs = Category.objects.all()
        
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        OrderByName = "a-z" #a-z/z-a
        OrderByAmt = "asc" #desc
        if 'OrderByName' in request.data:
            OrderByName = str(request.data['OrderByName']).strip()
        if 'OrderByAmt' in request.data:
            OrderByAmt = str(request.data['OrderByAmt']).strip()
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        orderby = ""
        if str(OrderByName).lower() == 'a-z':
            orderby = "Order By Invoice_documentlines.U_UTL_ITSBG asc"
        elif str(OrderByName).lower() == 'z-a':
            orderby = "Order By Invoice_documentlines.U_UTL_ITSBG desc"
        elif str(OrderByAmt).lower() == 'asc':
            orderby = "Order By LineTotal asc"
        elif str(OrderByAmt).lower() == 'desc':
            orderby = "Order By LineTotal desc"
        else:
            orderby = "Order By Invoice_documentlines.U_UTL_ITSBG asc"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        fromToDate = ""
        if str(FromDate) != "":
            fromToDate = f"AND Invoice_invoice.DocDate >= '{FromDate}' AND Invoice_invoice.DocDate <= '{ToDate}'"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
        mycursor = mydb.cursor(dictionary=True, buffered=True)
        # mycursor = db_connection.cursor()
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        TotalSales = 0

        dataContext = []
        for groupObj in categoryObjs:
            print("CategoryCode", groupObj.Number)
            sqlQuery = f"""
                SELECT Invoice_documentlines.`id`, Invoice_documentlines.U_UTL_ITSBG, 
                    sum(Invoice_documentlines.LineTotal) as LineTotal, 
                    sum(Invoice_documentlines.Quantity) as Quantity 
                FROM `Invoice_documentlines` 
                INNER Join Item_item ON Item_item.ItemCode = Invoice_documentlines.ItemCode 
                INNER Join Invoice_invoice ON Invoice_invoice.id = Invoice_documentlines.InvoiceID
                INNER Join BusinessPartner_businesspartner bp ON bp.CardCode = Invoice_invoice.CardCode
                WHERE 
                    Invoice_invoice.CancelStatus='csNo' 
                    AND Item_item.ItemsGroupCode = 1512
                    AND bp.U_U_UTL_Zone IN('{zonesStr}')
                    {fromToDate}
                GROUP BY Invoice_documentlines.`U_UTL_ITSBG` {orderby} LIMIT 10
            """
                    # AND Item_item.ItemsGroupCode = '{groupObj.Number}'
            # sqlQuery = "SELECT `ItemCode`, sum(`LineTotal`) FROM `Invoice_documentlines` GROUP BY `ItemCode`"

            print(sqlQuery)
            mycursor.execute(sqlQuery)
            itemList = mycursor.fetchall()
            # param_list = []
            # param_list.append(groupObj.Number)
            # param_list.append(f"'{zonesStr}'")
            # param_list.append(FromDate)
            # param_list.append(ToDate)
            # param_list.append(orderby)    
            # mycursor.callproc('ItemGroupSales', param_list)

            # itemList = Invoice_DocumentLines.objects.raw(sqlQuery)
            # print("itemList", itemList)
            # exit()
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            UnitPrice = 0
            totalPrice = 0
            totalQty = 0
            NoOfInvoice = len(itemList)
            print("NoOfInvoice", NoOfInvoice)
            if len(itemList) != 0:
                subGroupData = []
                for item in itemList:
                    U_UTL_ITSBG = str(item['U_UTL_ITSBG'])
                    UnitPrice   = float(item['LineTotal'])
                    Quantity    = int(item['Quantity'])
                    totalPrice  = totalPrice + UnitPrice
                    totalQty    = totalQty + Quantity

                    print("U_UTL_ITSBG", U_UTL_ITSBG)
                    
                    subGroup = {
                        "GroupName": U_UTL_ITSBG,
                        "GroupCode": groupObj.Number,
                        "TotalPrice": round(UnitPrice, 2),
                        "TotalQty": Quantity
                    }
                    subGroupData.append(subGroup)
                # endfor
                
                TotalSales = TotalSales + totalPrice
                bpData = {
                    "GroupName": groupObj.CategoryName,
                    "GroupCode": groupObj.Number,
                    "TotalPrice": round(totalPrice, 2),
                    "TotalQty": totalQty,
                    "SubGroup": subGroupData
                    # "NoOfInvoice": NoOfInvoice
                }
                dataContext.append(bpData)
            # endif

        allCreditNote = 0
            
        # endfor
        if 'PageNo' in request.data:
            PageNo = int(request.data['PageNo'])
            MaxSize = request.data['MaxSize']
            if MaxSize != "All":
                size = int(MaxSize)
                endWith = (PageNo * size)
                startWith = (endWith - size)
                dataContext = dataContext[startWith:endWith]

        return Response({"message": "Success","status": 200, "data":dataContext, "TotalSales": round(TotalSales, 2), "TotalCreditNote":-abs(allCreditNote)})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})
    

@api_view(['POST'])
def filter_item_dashboard_backup(request):
    try:
        # Filter = request.data['Filter']
        # SalesType = request.data['Type']
        FromDate = request.data['FromDate']
        ToDate = request.data['ToDate']
        SearchText = request.data['SearchText']

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        if str(SearchText).strip() != "":
            categoryObjs = Category.objects.filter(Q(CategoryName__icontains = SearchText))
        else:
            categoryObjs = Category.objects.all()
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        invIds = []
        if str(FromDate) != "":
            invIds = list(Invoice.objects.filter(CancelStatus="csNo", DocDate__gte = FromDate, DocDate__lte = ToDate).values_list('id', flat=True).distinct())    
        else:
            invIds = list(Invoice.objects.filter(CancelStatus="csNo").values_list('id', flat=True).distinct())
        invIdArr = ','.join(map(str, invIds))
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        TotalSales = 0

        dataContext = []
        for groupObj in categoryObjs:
            print("CategoryCode", groupObj.Number)
            # print("CategoryName", groupObj.CategoryName)
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # sqlQuery = f"SELECT Invoice_documentlines.id, Invoice_documentlines.ItemCode, Invoice_documentlines.ItemDescription, Invoice_documentlines.UnitPrice, Invoice_documentlines.Quantity, Invoice_documentlines.DiscountPercent FROM `Invoice_documentlines` LEFT Join Item_item ON Item_item.ItemCode = Invoice_documentlines.ItemCode WHERE Invoice_documentlines.InvoiceID in({invIdArr}); Item_item.ItemsGroupCode = '{groupObj.Number}'"

            sqlQuery = f"SELECT Invoice_documentlines.`id`, Invoice_documentlines.`ItemDescription`,Invoice_documentlines.ItemCode, sum(Invoice_documentlines.LineTotal) as LineTotal, sum(Invoice_documentlines.Quantity) as Quantity FROM `Invoice_documentlines` LEFT Join Item_item ON Item_item.ItemCode = Invoice_documentlines.ItemCode WHERE Item_item.ItemsGroupCode = '{groupObj.Number}' AND Invoice_documentlines.InvoiceID in({invIdArr}) GROUP BY Invoice_documentlines.ItemCode;"
            print(sqlQuery)
            itemList = Invoice_DocumentLines.objects.raw(sqlQuery)
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            UnitPrice = 0
            totalPrice = 0
            totalQty = 0
            if len(itemList) != 0:
                # NoOfInvoice = len(itemList)
                for item in itemList:
                    # ItemCode    = str(item.ItemCode)
                    UnitPrice   = float(item.LineTotal)
                    Quantity    = int(item.Quantity)
                    # DiscountPercent = float(item.DiscountPercent)
                    # baseAmount = (UnitPrice * Quantity)
                    # # print("befour discount baseAmount", baseAmount)
                    # if str(DiscountPercent) != '0.0':
                    #     temAmt = (baseAmount * DiscountPercent) / 100
                    #     baseAmount = (baseAmount - temAmt)
                    #     # print("after discount baseAmount", baseAmount)

                    totalPrice = totalPrice + UnitPrice
                    totalQty = totalQty + Quantity
                # endfor
                
                TotalSales = TotalSales + totalPrice
                bpData = {
                    "GroupName": groupObj.CategoryName,
                    "GroupCode": groupObj.Number,
                    "TotalPrice": round(totalPrice, 2),
                    "TotalQty": totalQty,
                    # "NoOfInvoice": NoOfInvoice
                }
                dataContext.append(bpData)
            # endif

        allCreditNote = 0
            
        # endfor
        if 'PageNo' in request.data:
            PageNo = int(request.data['PageNo'])
            MaxSize = request.data['MaxSize']
            if MaxSize != "All":
                size = int(MaxSize)
                endWith = (PageNo * size)
                startWith = (endWith - size)
                dataContext = dataContext[startWith:endWith]

        return Response({"message": "Success","status": 200, "data":dataContext, "TotalSales": round(TotalSales, 2), "TotalCreditNote":-abs(allCreditNote)})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})
    
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(['POST'])
def sold_items_dashboard(request):
    try:
        print(request.data)
        SearchText = request.data['SearchText']
        FromDate   = request.data['FromDate']
        ToDate     = request.data['ToDate']
        
        GroupCode = ""
        if 'GroupCode' in request.data:
            GroupCode  = request.data['GroupCode']
        
        SubGroupCode = ""
        if 'SubGroupCode' in request.data:
            SubGroupCode  = request.data['SubGroupCode']

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        OrderByName = "a-z" #a-z/z-a
        OrderByAmt = "" #desc
        if 'OrderByName' in request.data:
            OrderByName = str(request.data['OrderByName']).strip()
        if 'OrderByAmt' in request.data:
            OrderByAmt = str(request.data['OrderByAmt']).strip()
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        orderby = ""
        if str(OrderByName).lower() == 'a-z':
            orderby = "Order By Item_item.ItemName asc"
        elif str(OrderByName).lower() == 'z-a':
            orderby = "Order By Item_item.ItemName desc"
        elif str(OrderByAmt).lower() == 'asc':
            orderby = "Order By LineTotal asc"
        elif str(OrderByAmt).lower() == 'desc':
            orderby = "Order By LineTotal desc"
        else:
            orderby = "Order By Item_item.ItemName asc"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        fromToDate = ""
        if str(FromDate) != "":
            fromToDate = f"AND Invoice_invoice.DocDate >= '{FromDate}' AND Invoice_invoice.DocDate <= '{ToDate}'"

        allItems   = []
        TotalSales = 0
        sqlQuery = ""
        if str(GroupCode) != "":
            if str(SearchText) != "":
                sqlQuery = f"SELECT Invoice_documentlines.`id`, Invoice_documentlines.`ItemDescription`,Invoice_documentlines.ItemCode, sum(Invoice_documentlines.LineTotal) as LineTotal, sum(Invoice_documentlines.Quantity) as Quantity FROM `Invoice_documentlines` INNER Join Item_item ON Item_item.ItemCode = Invoice_documentlines.ItemCode INNER Join Invoice_invoice on Invoice_invoice.id = Invoice_documentlines.InvoiceID WHERE Invoice_invoice.CancelStatus='csNo' AND Item_item.ItemsGroupCode = '{GroupCode}' AND Invoice_documentlines.`ItemCode` like '%%{SearchText}%%' OR Invoice_documentlines.`ItemDescription` like '%%{SearchText}%%' {fromToDate} GROUP BY Invoice_documentlines.`ItemCode` {orderby}"
            else:
                sqlQuery = f"SELECT Invoice_documentlines.`id`, Invoice_documentlines.`ItemDescription`,Invoice_documentlines.ItemCode, sum(Invoice_documentlines.LineTotal) as LineTotal, sum(Invoice_documentlines.Quantity) as Quantity FROM `Invoice_documentlines` INNER Join Item_item ON Item_item.ItemCode = Invoice_documentlines.ItemCode INNER Join Invoice_invoice on Invoice_invoice.id = Invoice_documentlines.InvoiceID WHERE Invoice_invoice.CancelStatus='csNo' AND Item_item.ItemsGroupCode = '{GroupCode}' {fromToDate} GROUP BY Invoice_documentlines.`ItemCode` {orderby}"

        elif str(SubGroupCode) != "":
            if str(SearchText) != "":
                sqlQuery = f"SELECT Invoice_documentlines.`id`, Invoice_documentlines.`ItemDescription`,Invoice_documentlines.ItemCode, sum(Invoice_documentlines.LineTotal) as LineTotal, sum(Invoice_documentlines.Quantity) as Quantity FROM `Invoice_documentlines` INNER Join Item_item ON Item_item.ItemCode = Invoice_documentlines.ItemCode INNER Join Invoice_invoice on Invoice_invoice.id = Invoice_documentlines.InvoiceID WHERE Invoice_invoice.CancelStatus='csNo' AND Item_item.U_UTL_ITSBG = '{SubGroupCode}' AND Invoice_documentlines.`ItemCode` like '%%{SearchText}%%' OR Invoice_documentlines.`ItemDescription` like '%%{SearchText}%%' {fromToDate} GROUP BY Invoice_documentlines.`ItemCode` {orderby}"
            else:
                sqlQuery = f"SELECT Invoice_documentlines.`id`, Invoice_documentlines.`ItemDescription`,Invoice_documentlines.ItemCode, sum(Invoice_documentlines.LineTotal) as LineTotal, sum(Invoice_documentlines.Quantity) as Quantity FROM `Invoice_documentlines` INNER Join Item_item ON Item_item.ItemCode = Invoice_documentlines.ItemCode INNER Join Invoice_invoice on Invoice_invoice.id = Invoice_documentlines.InvoiceID WHERE Invoice_invoice.CancelStatus='csNo' AND Item_item.U_UTL_ITSBG = '{SubGroupCode}' {fromToDate} GROUP BY Invoice_documentlines.`ItemCode` {orderby}"
        else:
            if str(SearchText) != "":
                sqlQuery = f"SELECT Invoice_documentlines.`id`, Invoice_documentlines.`ItemDescription`,Invoice_documentlines.ItemCode, sum(Invoice_documentlines.LineTotal) as LineTotal, sum(Invoice_documentlines.Quantity) as Quantity FROM `Invoice_documentlines` INNER join Item_item ON Item_item.ItemCode = Invoice_documentlines.ItemCode INNER Join Invoice_invoice on Invoice_invoice.id = Invoice_documentlines.InvoiceID WHERE Invoice_invoice.CancelStatus='csNo' AND Invoice_documentlines.`ItemCode` like '%%{SearchText}%%' OR Invoice_documentlines.`ItemDescription` like '%%{SearchText}%%'  {fromToDate} GROUP BY Invoice_documentlines.`ItemCode` {orderby}"
            else:
                sqlQuery = f"SELECT Invoice_documentlines.`id`, Invoice_documentlines.`ItemDescription`,Invoice_documentlines.ItemCode, sum(Invoice_documentlines.LineTotal) as LineTotal, sum(Invoice_documentlines.Quantity) as Quantity FROM `Invoice_documentlines` INNER join Item_item ON Item_item.ItemCode = Invoice_documentlines.ItemCode INNER Join Invoice_invoice on Invoice_invoice.id = Invoice_documentlines.InvoiceID WHERE Invoice_invoice.CancelStatus='csNo' {fromToDate} GROUP BY Invoice_documentlines.`ItemCode` {orderby}"
            # endelse
        # endelse

        print(sqlQuery)
        itemList = Invoice_DocumentLines.objects.raw(sqlQuery)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        UnitPrice = 0
        totalPrice = 0
        totalQty = 0
        if len(itemList) != 0:
            # NoOfInvoice = len(itemList)
            for item in itemList:
                ItemCode        = str(item.ItemCode)
                if Item.objects.filter(ItemCode = ItemCode).exists():
                    itemObj     = Item.objects.filter(ItemCode = ItemCode).first()
                    UnitPrice   = float(item.LineTotal)
                    Quantity    = int(item.Quantity)
                    totalPrice  = totalPrice + UnitPrice
                    totalQty    = totalQty + Quantity

                    NoOfInvoice = 0
                    # TotalSales = TotalSales + totalPrice
                    avgPrice = 0
                    if totalQty > 0:
                        avgPrice = round(UnitPrice / Quantity, 2)
                        
                    contaxt = {
                        "ItemName"   : itemObj.ItemName,
                        "ItemCode"   : itemObj.ItemCode,
                        "UnitPrice"  : avgPrice,
                        "TotalPrice" : UnitPrice,
                        "TotalQty"   : Quantity,
                        "NoOfInvoice": NoOfInvoice
                    }
                    allItems.append(contaxt)

                print("ItemCode", ItemCode)
            # endfor
        # endif

        TotalSales = totalPrice
        allCreditNote = 0
            
        # endfor
        if 'PageNo' in request.data:
            PageNo = int(request.data['PageNo'])
            MaxSize = request.data['MaxSize']
            if MaxSize != "All":
                size = int(MaxSize)
                endWith = (PageNo * size)
                startWith = (endWith - size)
                allItems = allItems[startWith:endWith]

        return Response({"message": "Success","status": 200, "data":allItems, "TotalSales": round(TotalSales, 2), "TotalCreditNote":-abs(allCreditNote)})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})
    
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(["POST"])
def sold_items_dashboard_old(request):
    try:
        SearchText = request.data['SearchText']
        FromDate   = request.data['FromDate']
        ToDate     = request.data['ToDate']
        
        GroupCode = ""
        if 'GroupCode' in request.data:
            GroupCode  = request.data['GroupCode']

        allItems   = []
        invIds     = []
        
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        if str(FromDate) != "":
            invIds = list(Invoice.objects.filter(CancelStatus="csNo", DocDate__gte = FromDate, DocDate__lte = ToDate).values_list('id', flat=True).distinct())    
        else:
            invIds = list(Invoice.objects.filter(CancelStatus="csNo").values_list('id', flat=True).distinct())
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        itemList = ""
        if str(GroupCode) != "":
            itemCodeList = list(Item.objects.filter(ItemsGroupCode = GroupCode).values_list('ItemCode', flat=True).distinct())
            itemList = list(Invoice_DocumentLines.objects.filter(Q(ItemCode__in = itemCodeList) & Q(InvoiceID__in = invIds) & Q(Q(ItemCode__icontains = SearchText) | Q(ItemDescription__icontains = SearchText))).values_list('ItemCode', flat=True).distinct())
        else:
            itemList = list(Invoice_DocumentLines.objects.filter(Q(InvoiceID__in = invIds) & Q(Q(ItemCode__icontains = SearchText) | Q(ItemDescription__icontains = SearchText))).values_list('ItemCode', flat=True).distinct())
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        print("invIds >>>> >>> >> >", len(invIds))
        for item in itemList:
            UnitPrice = 0
            totalPrice = 0
            totalQty = 0

            print("item", item)
            if Item.objects.filter(ItemCode = item).exists():
                itemObj = Item.objects.filter(ItemCode = item).first()
                invItemObjs = Invoice_DocumentLines.objects.filter(InvoiceID__in = invIds, ItemCode = item).values('Quantity', 'UnitPrice', 'DiscountPercent')
                NoOfInvoice = len(invItemObjs.values_list('InvoiceID', flat=True).distinct())
                for itmObj in invItemObjs:  
                    UnitPrice = float(itmObj['UnitPrice'])
                    Quantity = int(itmObj['Quantity'])
                    DiscountPercent = float(itmObj['DiscountPercent'])
                    baseAmount = (UnitPrice * Quantity)
                    # print("befour discount baseAmount", baseAmount)
                    if str(DiscountPercent) != '0.0':
                        temAmt = (baseAmount * DiscountPercent) / 100
                        baseAmount = (baseAmount - temAmt)
                        # print("after discount baseAmount", baseAmount)

                    totalPrice = totalPrice + baseAmount
                    totalQty = totalQty + Quantity

                avgPrice = 0
                if totalQty > 0:
                    avgPrice = round(totalPrice / totalQty, 2)
                contaxt = {
                    "ItemName"   : itemObj.ItemName,
                    "ItemCode"   : itemObj.ItemCode,
                    "UnitPrice"  : avgPrice,
                    "TotalPrice" : totalPrice,
                    "TotalQty"   : totalQty,
                    "NoOfInvoice": NoOfInvoice
                }
                allItems.append(contaxt)
            # endif
        # endfor

        if 'PageNo' in request.data:
            PageNo = int(request.data['PageNo'])
            MaxSize = request.data['MaxSize']
            if MaxSize != "All":
                size = int(MaxSize)
                endWith = (PageNo * size)
                startWith = (endWith - size)
                allItems = allItems[startWith:endWith]

        return Response({"message": "Success", "status": 200, "data":allItems})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(["POST"])
def item_overview(request):
    try:
        allItems = []
        FromDate = request.data['FromDate']
        ToDate = request.data['ToDate']
        ItemCode = request.data['ItemCode']
        
        if Item.objects.filter(ItemCode = ItemCode).exists():
            itemObj = Item.objects.filter(ItemCode = ItemCode).first()

            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            invIds = []
            if str(FromDate) != "":
                invIds = list(Invoice.objects.filter(CancelStatus="csNo", DocDate__gte = FromDate, DocDate__lte = ToDate).values_list('id', flat=True).distinct())
            else:
                invIds = list(Invoice.objects.filter(CancelStatus="csNo").values_list('id', flat=True).distinct())
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # itemInvIds = (Invoice_DocumentLines.objects.filter(InvoiceID__in = invIds, ItemCode = ItemCode).values_list('InvoiceID', flat=True).distinct())
            invItemObjs = Invoice_DocumentLines.objects.filter(InvoiceID__in = invIds, ItemCode = ItemCode).order_by("id").values('InvoiceID', 'Quantity', 'UnitPrice','DiscountPercent')
            # print(invItemObjs.query)
            print(invItemObjs.values_list('InvoiceID', flat=True).distinct())
            NoOfInvoice = len(invItemObjs.values_list('InvoiceID', flat=True).distinct())
            UnitPrice  = 0
            totalPrice = 0
            totalQty   = 0
            item_invoice_ids = []
            ordList = []
            for itmObj in invItemObjs:
                item_invoice_ids.append(itmObj['InvoiceID'])
                UnitPrice = float(itmObj['UnitPrice'])
                Quantity = int(itmObj['Quantity'])
                DiscountPercent = float(itmObj['DiscountPercent'])
                baseAmount = (UnitPrice * Quantity)
                if str(DiscountPercent) != '0.0':
                    temAmt = (baseAmount * DiscountPercent) / 100
                    baseAmount = (baseAmount - temAmt)

                totalPrice = totalPrice + baseAmount
                totalQty = totalQty + Quantity
                
                invObj = Invoice.objects.get(pk = itmObj['InvoiceID'])
                ordContaxt = {
                    "CardCode": invObj.CardCode,
                    "CardName": invObj.CardName,
                    "InvoiceId":itmObj['InvoiceID'],
                    "UnitPrice": UnitPrice,
                    "Quantity": Quantity,
                    "DocTotal": baseAmount,
                    "Month": get_mm_yy(invObj.DocDate)
                }
                ordList.append(ordContaxt)
            MonthGroupSalesList = groupby(ordList, ['DocTotal', 'Month'], "Month", "DocTotal")
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            invIds = []
            if str(FromDate) != "":
                ordIds = list(Order.objects.filter(CancelStatus="csNo", DocDate__gte = FromDate, DocDate__lte = ToDate).values_list('id', flat=True).distinct())
            else:
                ordIds = list(Order.objects.filter(CancelStatus="csNo").values_list('id', flat=True).distinct())
            ordItemObjs = Order_DocumentLines.objects.filter(OrderID__in = ordIds, ItemCode = ItemCode).order_by("id").values('OrderID', 'Quantity', 'UnitPrice')
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            
            totalItemQty = 0
            totalItemPrice = 0
            pending_amount=0
            for ordObj in ordItemObjs:
                tempItemQty = int(ordObj['Quantity'])
                tempUnitPrice = int(ordObj['UnitPrice'])
                print("length", len(ordItemObjs))
                ordDocEntry = Order.objects.filter(pk = ordObj['OrderID']).values_list('DocEntry', flat=True)[0]
                print("length", ordDocEntry)
                if Invoice_DocumentLines.objects.filter(BaseEntry = ordDocEntry, ItemCode = ItemCode).exists():
                    tempInvObj = Invoice_DocumentLines.objects.filter(BaseEntry = ordDocEntry, ItemCode = ItemCode).values('id','Quantity', 'UnitPrice')[0]
                    print("hii", tempInvObj['id'])
                    tempInvQty = int(tempInvObj['Quantity'])
                    tempInvUnitPrice = int(tempInvObj['UnitPrice'])
                    if tempItemQty != tempInvQty:
                        qty = tempItemQty - tempInvQty
                        amount = qty * tempInvUnitPrice                        
                        pending_amount = pending_amount + amount
                        totalItemQty = totalItemQty + qty
                        totalItemPrice = totalItemPrice + amount
                elif Delivery_DocumentLines.objects.filter(BaseEntry = ordDocEntry, ItemCode = ItemCode).exists():
                    tempDelObj = Delivery_DocumentLines.objects.filter(BaseEntry = ordDocEntry, ItemCode = ItemCode).values('id','Quantity', 'UnitPrice')[0]
                    tempDelQty = int(tempDelObj['Quantity'])
                    tempDelUnitPrice = int(tempDelObj['UnitPrice'])
                    if tempItemQty != tempDelQty:
                        qty = tempItemQty - tempDelQty
                        amount = qty * tempDelUnitPrice                        
                        pending_amount = pending_amount + amount
                        totalItemQty = totalItemQty + qty
                        totalItemPrice = totalItemPrice + pending_amount
                else:
                    totalItemQty = tempItemQty
                    totalItemPrice = tempItemQty * tempItemQty
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            LastSalesDate = ""
            # NoOfInvoice = len(itemInvIds)
            if len(invItemObjs) != 0:
                # NoOfInvoice = len(invItemObjs)
                invID = invItemObjs.last()['InvoiceID']
                LastSalesDate = Invoice.objects.filter(pk = invID).values_list('DocDate', flat=True).first()
            
            avgPrice = round(totalPrice / totalQty, 2)
            contaxt = {
                "ItemName":itemObj.ItemName,
                "ItemCode":ItemCode,
                "UnitPrice":avgPrice,
                "TotalPrice": totalPrice,
                "TotalQty": totalQty,
                "NoOfInvoice": NoOfInvoice,
                "LastSalesDate": LastSalesDate,

                "TotalItemQty": totalItemQty,
                "TotalItemPrice": totalItemPrice,

                # "SaleOrder":ordList,
                # "BPGroupSalesList":BPGroupSalesList,
                "MonthGroupSalesList": MonthGroupSalesList
            }
             # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            allItems.append(contaxt)
            return Response({"message": "Success", "status": 200, "data":allItems})
        else:
            return Response({"message": "Invalid ItemCode", "status": 201, "data":[]})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})    
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(["POST"])
def item_invoices(request):
    try:
        allItems = []
        # CardCode = request.data['CardCode']
        FromDate = request.data['FromDate']
        ToDate = request.data['ToDate']
        ItemCode = str(request.data['ItemCode'])

        SearchText = ""
        if 'SearchText' in request.data:
            SearchText = str(request.data['SearchText']).strip()
            if str(SearchText) != "":
                SearchText = f"AND Invoice_invoice.CardName like '%%{SearchText}%%'"

        if Item.objects.filter(ItemCode = ItemCode).exists():
            itemObj = Item.objects.filter(ItemCode = ItemCode).first()
            CardCodes = []
            invJJ = []
            if str(FromDate) != "":
                invQuery = f"SELECT DISTINCT Invoice_invoice.CardCode, Invoice_invoice.id FROM `Invoice_invoice` INNER JOIN Invoice_documentlines on Invoice_invoice.id = Invoice_documentlines.InvoiceID WHERE Invoice_invoice.CancelStatus = 'csNo' AND Invoice_documentlines.ItemCode = '{ItemCode}' AND `DocDate` >= '{FromDate}' AND `DocDate` <= '{ToDate}' {SearchText}"
                invJJ = Invoice.objects.raw(invQuery)
                # print(invQuery)
            else:
                invQuery = f"SELECT DISTINCT Invoice_invoice.CardCode, Invoice_invoice.id FROM `Invoice_invoice` INNER JOIN Invoice_documentlines on Invoice_invoice.id = Invoice_documentlines.InvoiceID WHERE Invoice_invoice.CancelStatus = 'csNo' AND Invoice_documentlines.ItemCode = '{ItemCode}' {SearchText}"
                invJJ = Invoice.objects.raw(invQuery)
                # print(invQuery)

            for jj in invJJ:
                CardCodes.append(jj.CardCode)
            
            # CardCodes = list(set(CardCodes))
            print(CardCodes)
        
            totalPrice = 0
            totalQty   = 0
            ordList = []
            for cardCode in CardCodes:
                # print("cardCode", cardCode)
                bp_obj = BusinessPartner.objects.get(CardCode = cardCode)
                invIds = list(Invoice.objects.filter(CardCode = cardCode, CancelStatus="csNo").values_list('id', flat=True).distinct())
                # print(invIds)

                if Invoice_DocumentLines.objects.filter(InvoiceID__in = invIds, ItemCode = ItemCode).exists():
                    invItemObjs = Invoice_DocumentLines.objects.filter(InvoiceID__in = invIds, ItemCode = ItemCode).order_by("id").values('InvoiceID', 'Quantity', 'UnitPrice', 'DiscountPercent')
                    
                    bpTotalPrice = 0
                    bpTotalQty = 0
                    for itmObj in invItemObjs:
                        UnitPrice = float(itmObj['UnitPrice'])
                        Quantity = int(itmObj['Quantity'])
                        DiscountPercent = float(itmObj['DiscountPercent'])
                        baseAmount = (UnitPrice * Quantity)
                        # print("befour discount baseAmount", baseAmount)
                        if str(DiscountPercent) != '0.0':
                            temAmt = (baseAmount * DiscountPercent) / 100
                            baseAmount = (baseAmount - temAmt)
                            # print("after discount baseAmount", baseAmount)

                        bpTotalPrice = bpTotalPrice + baseAmount
                        bpTotalQty = bpTotalQty + Quantity

                    totalPrice = totalPrice + bpTotalPrice
                    totalQty = totalQty + bpTotalQty

                    ordContaxt = {
                        "CardCode": bp_obj.CardCode,
                        "CardName": bp_obj.CardName,
                        "TotalPrice": bpTotalPrice,
                        "TotalQty": bpTotalQty,
                    }
                    ordList.append(ordContaxt)
                # end if
            # end for

            if 'PageNo' in request.data:
                PageNo = int(request.data['PageNo'])
                MaxSize = request.data['MaxSize']
                if MaxSize != "All":
                    size = int(MaxSize)
                    endWith = (PageNo * size)
                    startWith = (endWith - size)
                    ordList = ordList[startWith:endWith]
            
            contaxt = {
                "ItemName" :itemObj.ItemName,
                "ItemCode" :ItemCode,
                "TotalPrice" : totalPrice,
                "TotalQty" : totalQty,
                "BPList"   :ordList,
            }    
            allItems.append(contaxt)
            return Response({"message": "Success", "status": 200, "data":allItems})
        else:
            return Response({"message": "Invalid ItemCode", "status": 201, "data":[]})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})
    
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(["POST"])
def bp_item_invoices(request):
    try:
        allItems = []
        CardCode = request.data['CardCode']
        ItemCode = request.data['ItemCode']
        FromDate = request.data['FromDate']
        ToDate = request.data['ToDate']
        if Item.objects.filter(ItemCode = ItemCode).exists():
            itemObj = Item.objects.filter(ItemCode = ItemCode).first()
            invIds = []
            if str(FromDate) != "":
                invIds = list(Invoice.objects.filter(CancelStatus="csNo", CardCode = CardCode, DocDate__gte = FromDate, DocDate__lte = ToDate).values_list('id', flat=True).distinct())
            else:
                invIds = list(Invoice.objects.filter(CancelStatus="csNo", CardCode = CardCode).values_list('id', flat=True).distinct())
                
            invItemObjs = Invoice_DocumentLines.objects.filter(InvoiceID__in = invIds, ItemCode = ItemCode).order_by("id").values('InvoiceID', 'Quantity', 'UnitPrice', 'LineTotal')
            UnitPrice  = 0
            totalPrice = 0
            totalQty   = 0
            ordList = []
            for itmObj in invItemObjs:
                LineTotal  = itmObj['LineTotal']
                UnitPrice  = itmObj['UnitPrice']
                Quantity   = itmObj['Quantity']
                # DocTotal   = int(UnitPrice) * int(Quantity)
                # totalPrice = totalPrice + (int(UnitPrice) * int(Quantity))
                totalPrice = totalPrice + float(LineTotal)
                totalQty   = totalQty + int(Quantity)

                # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                allPaymentsListBP = []
                invObj = Invoice.objects.filter(pk = itmObj['InvoiceID']).first()
                if str(FromDate) != "":
                    allPaymentsListBP = IncomingPaymentInvoices.objects.filter(InvoiceDocEntry = invObj.DocEntry, DocDate__gte = FromDate, DocDate__lte = ToDate).values_list('SumApplied', flat=True)
                else:
                    allPaymentsListBP = IncomingPaymentInvoices.objects.filter(InvoiceDocEntry = invObj.DocEntry).values_list('SumApplied', flat=True)

                # print("allPaymentsListBP", allPaymentsListBP)
                tempPayment = 0
                for item in allPaymentsListBP:
                    tempPayment += float(item)

                PaymentStatus = "Unpaid"
                if invObj.DocumentStatus == "bost_Close":
                    PaymentStatus = "Paid"
                elif len(allPaymentsListBP) != 0:
                    PaymentStatus = "Partially Paid"
                else:
                    PaymentStatus = "Unpaid"
                # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                ordContaxt = {
                    "InvoiceId":itmObj['InvoiceID'],
                    "DocEntry":invObj.DocEntry,
                    "UnitPrice": UnitPrice,
                    "Quantity": Quantity,
                    "DocTotal": LineTotal,
                    "CreateDate": invObj.DocDate,
                    "PaymentStatus": PaymentStatus,
                }
                ordList.append(ordContaxt)
            # end for
            bpobj = BusinessPartner.objects.filter(CardCode = CardCode).first()
            PayTermsGrpCode = bpobj.PayTermsGrpCode
            CreditLimit = bpobj.CreditLimit
            ptgcObj = PaymentTermsTypes.objects.filter(GroupNumber = PayTermsGrpCode).first()
            creditLimitDayes = ptgcObj.PaymentTermsGroupName

            GroupCode = bpobj.GroupCode
            GroupName = ""
            if BusinessPartnerGroups.objects.filter(Code = GroupCode).exists():
                bpGroup = BusinessPartnerGroups.objects.filter(Code = GroupCode).first()
                GroupName = bpGroup.Name

            GSTIN = ""
            BPAddress = ""
            if BPBranch.objects.filter(BPCode = CardCode).exists():
                bpBranch = BPBranch.objects.filter(BPCode = CardCode).first()
                GSTIN = str(bpBranch.GSTIN)
                BPAddress = f"{bpBranch.Street} {bpBranch.City} {bpBranch.ZipCode}"
            contaxt = {
                "ItemName":itemObj.ItemName,
                "ItemCode":ItemCode,
                "CardName": bpobj.CardName,
                "CardCode": bpobj.CardCode,
                "EmailAddress": bpobj.EmailAddress,
                "Phone1": bpobj.Phone1,
                "GSTIN": GSTIN,
                "BPAddress": BPAddress,
                "GroupName": GroupName,
                "CreditLimit": CreditLimit,
                "CreditLimitDayes": creditLimitDayes,
                "TotalPrice": totalPrice,
                "TotalQty": totalQty,
                "SaleOrder":ordList,
            }    
            allItems.append(contaxt)
            return Response({"message": "Success", "status": 200, "data":allItems})
        else:
            return Response({"message": "Invalid ItemCode", "status": 201, "data":[]})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})
    
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>