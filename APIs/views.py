from django.shortcuts import render
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status, generics
from .models import user, role, event, parking, grievance, category, vehicleType, parkingTransaction, beatBox, foundItem, lostItem, facilities, medicalFacility, foodDistribution, washroom, shoeStand, dayWiseRitual, timeWiseRitual, parkingTransaction, imageStorage, hotels, waterSpots
from .serializers import grievanceSerializer, parkingTransactionSerializer, foundItemSerializer, lostItemSerializer, userSerializer, imageStorageSerializer, hotelSerializer
from datetime import datetime
from rest_framework.decorators import api_view
#from django.forms.models import model_to_dict
from django.core import serializers
import jwt
import json
"""import string
import random"""
#import uuid
import base64
from PIL import Image
import io
from . import colsReq
# from azure.storage.blob import BlobClient, BlobServiceClient
import base64
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from . import token

baseURL = "https://rathyatrabackend.azurewebsites.net/static/image/"

def eventCheck(id):
    print(id)
    return event.objects.get(eventId = id).activeFlag

def getData(data):
    return base64.b64decode(data)

def b64ToJson(data):
    return base64.b64encode(data).decode("utf-8")

def getVehicleType(id):
    vcl = vehicleType.objects.get(vehicleTypeId = id)
    return vcl.vehicleType

def getCategory(id):
    cat = category.objects.get(categoryId = id)
    return [cat.categoryName, cat.categoryNameO, cat.categoryType, cat.categoryTypeO, cat.priority, cat.priorityO]

def getRole(token):
    decoded = jwt.decode(token, verify=False, algorithms=["HS256"], options={"verify_signature": False}) 
    userName = decoded.get("userName")
    password = decoded.get("password")
    u = list(user.objects.filter(userName = userName).values())[0]
    e = event.objects.get(eventId = u["eventId"])
    if e.activeFlag:
        if u["password"] == password:
            r = role.objects.get(roleId = u["roleId"])
            u["role"] = r.roleName
            del u["password"]
            del u["eventId"]
            del u["roleId"]
            del u["modifyDate"]
            del u["createDate"]
            u["token"] = jwt.encode(payload= u, key='rath', algorithm="HS256") 
            return u
        else:
            return "Invalid User"
    else:
        return "Invalid User"

def completeProfile(data):
    userName = data.get("userName")
    password = data.get("password")
    u = list(user.objects.filter(userName = userName).values())[0]
    e = event.objects.get(eventId = u["eventId"])
    if e.activeFlag:
        if u["password"] == password:
            r = role.objects.get(roleId = u["roleId"])
            u["role"] = r.roleName
            del u["password"]
            del u["eventId"]
            del u["roleId"]
            del u["modifyDate"]
            del u["createDate"]
            u["token"] = jwt.encode(payload= u, key='rath', algorithm="HS256") 
            return u
        else:
            return Response({"message":"Invalid User"}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({"message":"Event no longer Exist"}, status=status.HTTP_401_UNAUTHORIZED)

# # #generate random string

def getID():
    d = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')[:-3]
    id = abs(hash(d)) % (10 ** 8)
    return id

#<-------------------------------Image------------------------------->#

@api_view(["POST"])
def imageUpload(request):
    print(request)
    print("1",request.FILES["image"])
    img = base64.b64encode(request.FILES["image"].file.read()).decode()
    print("2",len(img))
    imageUp = imageStorage.objects.create(eventId = "1", functionName = "lost", token = "1234", image = img, modifyDate = datetime.now())
    # print("3",imageUp)
    return HttpResponse(json.dumps({'message': "Uploaded"}), status=200)

@api_view(["GET"])
def getImage(request):
    tk = request.data.get("token")
    """print(tk)"""
    res = list(imageStorage.objects.filter(token = tk).values())
    return Response({"data": res})

#<-------------------------------Parking Transaction------------------------------->#

@api_view(["GET"])
def getParkingTransaction(request):
    res = parkingTransaction.objects.all().values()
    return Response({"data": res})

#<-------------------------------Beat Box------------------------------->#
#implement language filter
@api_view(["GET"])
def getBeatBox(request):
    res = beatBox.objects.all().values()
    return Response({"data": res})

#<-------------------------------Login------------------------------->#

# @api_view(["DELETE"])
@api_view(["GET"])
def deleteData(request, page, date):
    print(page,date)
    # res = imageStorage.objects.filter(token = 123).delete()
    # setattr(res, "beatBoxId", "")
    # res.save()
    return Response(date)

@api_view(["POST"])
def login(request):
    data = request.data
    profile = list(user.objects.filter(contactNumber = data["contactNumber"]).values())
    print(profile)
    if len(profile) == 0:
        return Response({'message':"Number not Rgistered",'error':True,'code':401}, status= status.HTTP_401_UNAUTHORIZED)
    ro = {"1": "Police", "2":"Parking", "3":"General User"}
    profile = profile[0]
    print(profile)
    if getData(profile["password"]).decode("utf-8") == getData(data["password"]).decode("utf-8"):
        if eventCheck(profile["eventId"]):
            prf = profile
            del profile["password"]
            del prf["createDate"]
            del prf["modifyDate"]
            profile["token"] = jwt.encode(payload= prf, key='rath', algorithm="HS256")
            profile["role"] = ro[profile["roleId"]]
            if profile["roleId"] == "2":
                profile["parkingDetail"] = list(parking.objects.filter(userId = profile["userId"]).values())[0]["parkingId"]
            del profile["roleId"]
            del profile["eventId"]
            return Response({'data':profile,'message': "Login Successful",'error':False,'code':200}, status= status.HTTP_200_OK)
        else:
            return Response({'message':"Event Ended",'error':True,'code':403}, status= status.HTTP_403_FORBIDDEN)
    else:
        return Response({'message':"Password Mismatch",'error':True,'code':401}, status= status.HTTP_401_UNAUTHORIZED)
    # if len(profile) > 1:
    #     i = 0        
    #     while i < len(profile):
    #         if getData(profile[i]["password"]).decode("utf-8") == getData(data["password"]).decode("utf-8"):
    #             if eventCheck(profile[i]["eventId"]):
    #                 prf = profile
    #                 del prf["createDate"]
    #                 del prf["modifyDate"]
    #                 profile["token"] = jwt.encode(payload= prf, key='rath', algorithm="HS256")
    #                 profile[i]["role"] = ro[profile[i]["roleId"]]
    #                 if profile[i]["roleId"] == "2":
    #                     profile["parkingDetail"] = list(parking.objects.filter(userId = profile["userId"]).values())[0]["parkingId"]
    #                 del profile[i]["roleId"]
    #                 del profile[i]["eventId"]
    #                 del profile[i]["password"]
    #                 return Response({'message':profile[i],'error':False,'code':200}, status= status.HTTP_200_OK)
    #             else:
    #                 return Response({'message':"Event Ended",'error':True,'code':403}, status= status.HTTP_403_FORBIDDEN)
    #         else:
    #             return Response({'message':"Password Mismatch",'error':True,'code':401}, status= status.HTTP_401_UNAUTHORIZED)
    # else:
    #     profile = profile[0]
    #     print(profile)
    #     if getData(profile["password"]).decode("utf-8") == getData(data["password"]).decode("utf-8"):
    #         if eventCheck(profile["eventId"]):
    #             prf = profile
    #             del prf["createDate"]
    #             del prf["modifyDate"]
    #             profile["token"] = jwt.encode(payload= prf, key='rath', algorithm="HS256")
    #             profile["role"] = ro[profile["roleId"]]
    #             if profile["roleId"] == "2":
    #                 profile["parkingDetail"] = list(parking.objects.filter(userId = profile["userId"]).values())[0]["parkingId"]
    #             del profile["roleId"]
    #             del profile["eventId"]
    #             del profile["password"]
    #             return Response({'message':profile,'error':False,'code':200}, status= status.HTTP_200_OK)
    #         else:
    #             return Response({'message':"Event Ended",'error':True,'code':403}, status= status.HTTP_403_FORBIDDEN)
    #     else:
    #         return Response({'message':"Password Mismatch",'error':True,'code':401}, status= status.HTTP_401_UNAUTHORIZED)
    # print(data["userName"])
    # user = completeProfile(data)
    # if user["role"] == "Parking":
    #     parkingDetail = list(parking.objects.filter(userId = user["userId"]).values())[0]["parkingId"]
    #     print(parkingDetail)
    #     user["parkingDetail"] = parkingDetail
    # return Response(user)

@api_view(["POST"])
def generalUserRegistration(request):
    vaildator = getData(request.META["HTTP_VALIDATOR"]).decode("utf-8")
    print(str(vaildator))
    if str(vaildator) != token.userRegistration():
        return Response({"message": "Validation Fialed", 'error':True,'code':404}, status= status.HTTP_404_NOT_FOUND)
    data = json.loads(getData(request.data.get("data")))
    data = data.get("data")
    eventId = len(list(event.objects.all().values()))
    data["eventId"] = eventId
    data["roleId"] = 3
    data["modifyDate"] = datetime.now()
    print(data)
    # print(list(user.objects.filter(contactNumber = data["contactNumber"]).values()))
    if len(list(user.objects.filter(contactNumber = data["contactNumber"]).values())) != 0:
        return Response({"message": "Number Alredy Registered", 'error':True,'code':404}, status= status.HTTP_400_BAD_REQUEST)
    serializer = userSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        del serializer.data["password"]
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#<-------------------------------category------------------------------->#
@api_view(["GET"])
def getCtegory(request):
    obj = list(category.objects.all().values())
    return Response({"data": obj})

#<-------------------------------parking------------------------------->#
# from django.db.models import Subquery, OuterRef
@api_view(["GET"])
def prkng(request):
    prkng = parking.objects.filter(eventId = 1).filter(activeFlag = True).order_by('id')
    res = {}
    vType = ["Bike", "Car", "Bus", "Shuttle"]
    for i in range(1, 5):
        res[vType[i - 1]] = list(prkng.filter(vehicleTypeId = i).values())
    lang = request.headers.get("language")
    if lang == "Odia":
        for key, value in res.items():
            for i in range(len(value)):
                res[key][i]["parkingName"] = res[key][i]["parkingNameO"]
                res[key][i]["location"] = res[key][i]["locationO"]
    return Response({"data": res})

@api_view(["GET"])
def getParking(request, page):
    prkng = list(parking.objects.filter(activeFlag = True).order_by('id').values())
    # print(prkng)
    lang = request.headers.get("language")
    i = 0
    res = []
    ls = []
    while i < len(prkng):
        elem = prkng[i]   
        # print(i, elem)
        fac = list(facilities.objects.filter(facilityTypeId = elem["id"]).filter(facilityType = "Parking").values())
        id = elem["eventId"]
        del prkng[i]["eventId"]
        if not eventCheck(id):
            prkng.pop(i)
        else:
            id = elem["vehicleTypeId"]
            del prkng[i]["vehicleTypeId"]
            prkng[i]["vehicleType"] = getVehicleType(id)
            prkng[i]["imageURL"] = baseURL + "parking/" + str(prkng[i]["parkingId"]) + ".jpg"
            # prkng[i]["image"] = "image base64"
            if prkng[i]["parkingId"] in ls:
                inx = ls.index(prkng[i]["parkingId"])
                temp = res[inx]
                if "facilities" not in temp:
                    res[inx]["facilities"]  = fac
                if lang != "Odia":
                    temp[prkng[i]["vehicleType"] + "Capacity"] = prkng[i]["capacity"]
                    temp[prkng[i]["vehicleType"] + "Vacancy"] = prkng[i]["vacancy"]
                    temp[prkng[i]["vehicleType"] + "Charge"] = prkng[i]["charge"]
                else:
                    temp[prkng[i]["vehicleType"] + "CapacityO"] = prkng[i]["capacityO"]
                    temp[prkng[i]["vehicleType"] + "VacancyO"] = prkng[i]["vacancyO"]
                    temp[prkng[i]["vehicleType"] + "ChargeO"] = prkng[i]["chargeO"]
                res[inx] = temp
            else:                 
                vt = prkng[i]["vehicleType"]
                prkng[i][vt + "Capacity"] = prkng[i]["capacity"]
                del prkng[i]["capacity"]
                prkng[i][vt + "Vacancy"] = prkng[i]["vacancy"]
                del prkng[i]["vacancy"]
                prkng[i][vt + "Charge"] = prkng[i]["charge"]
                del prkng[i]["charge"]
                if lang == "Odia":
                    prkng[i]["parkingName"] = prkng[i]["parkingNameO"]
                    prkng[i]["openingTime"] = prkng[i]["openingTimeO"]
                    prkng[i]["closingTime"] = prkng[i]["closingTimeO"]
                    prkng[i]["location"] = prkng[i]["locationO"]
                prkng[i]["facilities"] = fac
                res.append(prkng[i])
                ls.append(prkng[i]["parkingId"])
            i +=1
    paginator = Paginator(res, per_page=20)
    res = list(paginator.get_page(page))
    return Response({"data": res, "count": paginator.count})

@api_view(["POST"])
def getParkingList(request):    
    parkingIds = request.data.get("parkingDetail")
    prkng = []
    for id in parkingIds:
        prkng += list(parking.objects.filter(parkingId = id).values())
    lang = request.headers.get("language")
    i = 0
    res = []
    ls = []
    print(prkng)
    while i < len(prkng):
        elem = prkng[i]
        fac = list(facilities.objects.filter(facilityTypeId = elem["id"]).filter(facilityType = "Parking").values())
        # print(elem)        
        id = elem["eventId"]
        del prkng[i]["eventId"]
        if not eventCheck(id):
            prkng.pop(i)
        else:
            id = elem["vehicleTypeId"]
            del prkng[i]["vehicleTypeId"]
            prkng[i]["vehicleType"] = getVehicleType(id)
            # prkng[i]["imageURL"] = baseURL + "parking/" + str(prkng[i]["parkingId"]) + ".jpg"
            # prkng[i]["image"] = "image base64"
            if prkng[i]["parkingId"] in ls:
                inx = ls.index(prkng[i]["parkingId"])
                temp = res[inx]
                if "facilities" not in temp:
                    res[inx]["facilities"]  = fac
                temp[prkng[i]["vehicleType"] + "Capacity"] = prkng[i]["capacity"]
                temp[prkng[i]["vehicleType"] + "Vacancy"] = prkng[i]["vacancy"]
                temp[prkng[i]["vehicleType"] + "Charge"] = prkng[i]["charge"]
                res[inx] = temp
            else:            
                vt = prkng[i]["vehicleType"]
                prkng[i][vt + "Capacity"] = prkng[i]["capacity"]
                del prkng[i]["capacity"]
                prkng[i][vt + "Vacancy"] = prkng[i]["vacancy"]
                del prkng[i]["vacancy"]
                prkng[i][vt + "Charge"] = prkng[i]["charge"]
                del prkng[i]["charge"]
                if lang == "Odia":
                    prkng[i]["parkingName"] = prkng[i]["parkingNameO"]
                    prkng[i]["openingTime"] = prkng[i]["openingTimeO"]
                    prkng[i]["closingTime"] = prkng[i]["closingTimeO"]
                    prkng[i]["location"] = prkng[i]["locationO"]
                prkng[i]["facilities"] = fac
                res.append(prkng[i])
                ls.append(prkng[i]["parkingId"])
            i +=1

    return Response({"data": res})

@api_view(["GET"])
def getParkingById(request, id):    
    try:
        prkng = list(parking.objects.filter(parkingId = id).values())
    except:
        return Response({"message": "ID doesn't exist", 'error': True}, status=status.HTTP_404_NOT_FOUND)
    lang = request.headers.get("language")
    i = 0
    res = []
    ls = []
    while i < len(prkng):
        elem = prkng[i]
        fac = list(facilities.objects.filter(facilityTypeId = elem["id"]).filter(facilityType = "Parking").values())
        # print(elem)        
        id = elem["eventId"]
        del prkng[i]["eventId"]
        if not eventCheck(id):
            prkng.pop(i)
        else:
            id = elem["vehicleTypeId"]
            del prkng[i]["vehicleTypeId"]
            prkng[i]["vehicleType"] = getVehicleType(id)
            prkng[i]["imageURL"] = baseURL + "parking/" + str(prkng[i]["parkingId"]) + ".jpg"
            # prkng[i]["image"] = "image base64"
            if prkng[i]["parkingId"] in ls:
                inx = ls.index(prkng[i]["parkingId"])
                temp = res[inx]
                if "facilities" not in temp:
                    res[inx]["facilities"]  = fac
                temp[prkng[i]["vehicleType"] + "Capacity"] = prkng[i]["capacity"]
                temp[prkng[i]["vehicleType"] + "Vacancy"] = prkng[i]["vacancy"]
                temp[prkng[i]["vehicleType"] + "Charge"] = prkng[i]["charge"]
                res[inx] = temp
            else:            
                vt = prkng[i]["vehicleType"]
                prkng[i][vt + "Capacity"] = prkng[i]["capacity"]
                del prkng[i]["capacity"]
                prkng[i][vt + "Vacancy"] = prkng[i]["vacancy"]
                del prkng[i]["vacancy"]
                prkng[i][vt + "Charge"] = prkng[i]["charge"]
                del prkng[i]["charge"]
                if lang == "Odia":
                    prkng[i]["parkingName"] = prkng[i]["parkingNameO"]
                    prkng[i]["openingTime"] = prkng[i]["openingTimeO"]
                    prkng[i]["closingTime"] = prkng[i]["closingTimeO"]
                    prkng[i]["location"] = prkng[i]["locationO"]
                prkng[i]["facilities"] = fac
                res.append(prkng[i])
                ls.append(prkng[i]["parkingId"])
            i +=1

    return Response({"data": res[0]})

@api_view(["PUT"])
def updateParkingById(request):
    user = request.headers.get("Authorization")
    lang = request.headers.get("language")
    user = jwt.decode(user, verify=False, algorithms=["HS256"], options={"verify_signature": False}) 
    if user["roleId"] == "2":
        id = request.data.get("id")
        increase = request.data.get("increase")
        vt = request.data.get("vehicleType")
        vtId = list(vehicleType.objects.filter(vehicleType = vt).values())[0]["vehicleTypeId"]
        try:
            obj = parking.objects.filter(parkingId = id).filter(vehicleTypeId = vtId)
        except:
            return Response({"message": "ID doesn't exist", 'error': True}, status=status.HTTP_404_NOT_FOUND)
        obj1 = list(obj.values())[0]
        if increase == "true":
            vacancy = obj1.get("vacancy") + 1
            if vacancy > obj1.get("capacity"):
                return Response({"message": "Capacity Issue", 'error': True, 'status': 406}, status=status.HTTP_406_NOT_ACCEPTABLE)
            data = {"eventId": obj1.get("eventId"),
                "createDate": datetime.now(),
                "parkingId": obj1.get("parkingId"),
                "vehicleTypeId": obj1.get("vehicleTypeId"),
                "out": True
            }
            serializer = parkingTransactionSerializer(data  =data)
            if serializer.is_valid():
                serializer.save()
        else:
            vacancy = obj1.get("vacancy") - 1
            if vacancy < 0:
                return Response({"message": "No more vaccancy", 'error': True, 'status': 406}, status=status.HTTP_406_NOT_ACCEPTABLE)
            data = {"eventId": obj1.get("eventId"),
                "createDate": datetime.now(),
                "parkingId": obj1.get("parkingId"),
                "vehicleTypeId": obj1.get("vehicleTypeId"),
                "out": False
            }
            serializer = parkingTransactionSerializer(data = data)
            if serializer.is_valid():
                serializer.save()
        obj.update( vacancy = vacancy)
        obj.update( vacancyO = vacancy)
        obj = serializers.serialize('json', obj)
        obj = obj.strip('][')
        data = json.loads(obj)["fields"]
        return Response({'message':data,'error':False,'code':200}, status= status.HTTP_200_OK)
    else:
        return Response({'message':'Unauthorize Access!!','error':True,'code':401,'result':{'totalItems':0,'items':[],'totalPages':0,'currentPage':0}}, status= status.HTTP_401_UNAUTHORIZED)

#<-------------------------------Grievance------------------------------->#
@api_view(["GET"])
def getGrievance(request, page, date):
    user = request.headers.get("Authorization")
    language = request.headers.get("language")
    user = jwt.decode(user, verify=False, algorithms=["HS256"], options={"verify_signature": False}) 
    print(user)
    if user["roleId"] == "1":
        sosLst1 = grievance.objects.all().order_by('-createDate')
        if date != " ":
            import datetime
            sosLst1 = sosLst1.filter(createDate__range = (datetime.datetime.combine(datetime.datetime.strptime(date, "%Y-%m-%d"), datetime.time.min),
                            datetime.datetime.combine(datetime.datetime.strptime(date, "%Y-%m-%d"), datetime.time.max)))
        sosLst1 = sosLst1.values()
        if len(list(sosLst1)) == 0:
            return Response({'data':[],'count': 0})
        paginator = Paginator(sosLst1, per_page=20)
        sosLst = list(paginator.get_page(page))
        # pageC = int(paginator.count / 20)
        # if int(paginator.count % 20) > 0:
        #     pageC += 1
        # if int(page) > pageC:
        #     return Response({'message':'No Data','error':True,'code':404}, status= status.HTTP_404_NOT_FOUND)
        i = 0
        while i < len(sosLst):
            elem = sosLst[i]
            if "eventId_id" in elem:
                id = elem["eventId_id"]
                del sosLst[i]["eventId_id"]
            else:
                id = elem["eventId"]
                del sosLst[i]["eventId"]
            if not eventCheck(id):
                sosLst.pop(i)
            else:
                if "categoryId_id" in elem:
                    id = elem["categoryId_id"]
                    del sosLst[i]["categoryId_id"]
                else:
                    id = elem["categoryId"]
                    del sosLst[i]["categoryId"]
                catLs = getCategory(id)
                if language == "Odia":                    
                    sosLst[i]["categoryName"] = catLs[1]
                    sosLst[i]["categoryType"] = catLs[3]
                    sosLst[i]["priority"] = catLs[5]
                else:
                    sosLst[i]["categoryName"] = catLs[0]
                    sosLst[i]["categoryType"] = catLs[2]
                    sosLst[i]["priority"] = catLs[4]
                sosLst[i]["image"] = list(imageStorage.objects.filter(functionName = "grievance").filter(token = sosLst[i]["token"]).values())
                i += 1   
        return Response({"data": sosLst, "count": paginator.count})
    else:
        return Response({'message':'Unauthorize Access!!','error':True,'code':401,'result':{'totalItems':0,'items':[],'totalPages':0,'currentPage':0}}, status= status.HTTP_401_UNAUTHORIZED)
    
@api_view(["GET"])
def getGrievanceById(request, id):
    user = request.headers.get("Authorization")
    language = request.headers.get("language")
    user = jwt.decode(user, verify=False, algorithms=["HS256"], options={"verify_signature": False}) 
    if user["roleId"] == "1":
        try:
            sosLst = list(grievance.objects.filter(grievanceId = id).values())
        except:
            return Response({"message": "ID doesn't exist", 'error': True}, status=status.HTTP_404_NOT_FOUND)
        print(sosLst)
        i = 0
        while i < len(sosLst):
            elem = sosLst[i]
            if "eventId_id" in elem:
                id = elem["eventId_id"]
                del sosLst[i]["eventId_id"]
            else:
                id = elem["eventId"]
                del sosLst[i]["eventId"]
            if not eventCheck(id):
                sosLst.pop(i)
            else:
                if "categoryId_id" in elem:
                    id = elem["categoryId_id"]
                    del sosLst[i]["categoryId_id"]
                else:
                    id = elem["categoryId"]
                    del sosLst[i]["categoryId"]
                catLs = getCategory(id)
                if language == "Odia":                    
                    sosLst[i]["categoryName"] = catLs[1]
                    sosLst[i]["categoryType"] = catLs[3]
                    sosLst[i]["priority"] = catLs[5]
                else:
                    sosLst[i]["categoryName"] = catLs[0]
                    sosLst[i]["categoryType"] = catLs[2]
                    sosLst[i]["priority"] = catLs[4]
                sosLst[i]["image"] = list(imageStorage.objects.filter(functionName = "grievance").filter(token = sosLst[i]["token"]).values())
                i += 1                
        return Response({"data": sosLst[0]})
    else:
        return Response({'message':'Unauthorize Access!!','error':True,'code':401,'result':{'totalItems':0,'items':[],'totalPages':0,'currentPage':0}}, status= status.HTTP_401_UNAUTHORIZED)

@api_view(["POST"])
def postGrievance(request):
    # print(request)
    # print(request.META["HTTP_VALIDATOR"])
    vaildator = getData(request.META["HTTP_VALIDATOR"]).decode("utf-8")
    print(str(vaildator))
    if str(vaildator) != token.postGrievance():
        return Response({"message": "Validation Fialed", 'error':True,'code':404}, status= status.HTTP_404_NOT_FOUND)
    data = json.loads(getData(request.data.get("data")))
    eventName = data.get("eventName")
    language = request.headers.get("language")
    cat = data.get("category")
    print(language, cat)
    data = data.get("data")
    eventId = event.objects.get(eventName = eventName).eventId
    try:
        id = category.objects.get(categoryName = cat).categoryId
    except:
        return Response({'message':'Category not found','error':True,'code':404,'result':{'totalItems':0,'items':[],'totalPages':0,'currentPage':0}}, status= status.HTTP_404_NOT_FOUND)
    print(id)
    data["imageURL"] = ""
    data["categoryId"] = id
    data["eventId"] = eventId
    data["status"] = "Open"
    data["token"] = getID()
    data["modifyDate"] = datetime.now()    
    if "image" in data and data["image"] != "":
        for i in range(len(data["image"])):
            #"image": [<base64>, <base64>, <base64>]
            image = data["image"][i]
            imageUp = imageStorage.objects.create(eventId = "1", functionName = "grievance", token = data["token"], image = image, modifyDate = datetime.now())
    
    serializer = grievanceSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["PUT"])
def updateGrievanceById(request):
    vaildator = getData(request.META["HTTP_VALIDATOR"]).decode("utf-8")
    print(str(vaildator))
    if str(vaildator) != token.updateGrivance():
        return Response({"message": "Validation Fialed", 'error':True,'code':404}, status= status.HTTP_404_NOT_FOUND)
    data = json.loads(getData(request.data.get("data")))
    id = data.get("id")
    data = data.get("data")
    try:
        obj = grievance.objects.get(grievanceId = id)
    except:
        return Response({"message": "ID doesn't exist", 'error': True}, status=status.HTTP_404_NOT_FOUND)
    keys = list(data.keys())
    for i in range(len(keys)):
        setattr(obj, keys[i], data[keys[i]])
    obj.save()
    return Response({'message':'Updated Successfully','error':False,'code':200}, status= status.HTTP_200_OK)

@api_view(["POST"])
def filterGrievanceItem(request, page):
    data = json.loads(getData(request.data.get("data")))
    user = request.headers.get("Authorization")
    user = jwt.decode(user, verify=False, algorithms=["HS256"], options={"verify_signature": False})
    # print(user, type(data))
    if user["roleId"] == "1":
        obj = ""
        # print(data["categoryId"])
        print(type(data["token"]))
        if data["token"] != "":
            if obj == "":
                obj = grievance.objects.filter(token = data["token"])
            else:
                obj = obj.filter(token = data["token"])
            print(obj)
        if data["categoryName"] != "":
            id = category.objects.get(categoryName = data["categoryName"]).categoryId
            if obj == "":
                obj = grievance.objects.filter(categoryId = id)
            else:
                obj = obj.filter(categoryId = id)
            print(obj.values())
        if data["status"] != "":
            if obj == "":
                obj = grievance.objects.filter(status = data["status"])
            else:
                obj = obj.filter(status = data["status"])
            print(obj)
        if data["phoneNumber"] != "":
            if obj == "":
                obj = grievance.objects.filter(primaryNumber = str(data["phoneNumber"]))
            else:
                obj = obj.filter(primaryNumber = str(data["phoneNumber"]))
            # print(obj)
        if data["fromDate"] != "":
            print(obj)
            import datetime
            if obj == "":
                # obj = foundItem.objects.filter(createDate = data["createDate"])
                obj = grievance.objects.filter(createDate__range = (datetime.datetime.combine(datetime.datetime.strptime(data["fromDate"], "%Y-%m-%dT%H:%M"), datetime.time.min),
                            datetime.datetime.combine(datetime.datetime.strptime(data["toDate"], "%Y-%m-%dT%H:%M"), datetime.time.max)))
            else:
                obj = obj.filter(createDate__range = (datetime.datetime.combine(datetime.datetime.strptime(data["fromDate"], "%Y-%m-%dT%H:%M"), datetime.time.min),
                            datetime.datetime.combine(datetime.datetime.strptime(data["toDate"], "%Y-%m-%dT%H:%M"), datetime.time.max)))
        sosLst = list(obj.order_by("-createDate").values())
        paginator = Paginator(sosLst, per_page=20)
        sosLst = list(paginator.get_page(page))
        # print(list(obj))
        # print(len(list(obj)))
        i = 0
        language = request.headers.get("language")
        while i < len(sosLst):
            elem = sosLst[i]
            id = elem["eventId"]
            del sosLst[i]["eventId"]
            if not eventCheck(id):
                sosLst.pop(i)
            else:
                id = elem["categoryId"]
                del sosLst[i]["categoryId"]
                catLs = getCategory(id)
                if language == "Odia":                    
                    sosLst[i]["categoryName"] = catLs[1]
                    sosLst[i]["categoryType"] = catLs[3]
                    sosLst[i]["priority"] = catLs[5]
                else:
                    sosLst[i]["categoryName"] = catLs[0]
                    sosLst[i]["categoryType"] = catLs[2]
                    sosLst[i]["priority"] = catLs[4]
                sosLst[i]["image"] = list(imageStorage.objects.filter(functionName = "grievance").filter(token = sosLst[i]["token"]).values())
                i += 1                
        return Response({"data": sosLst, "count": paginator.count})
        # return Response({"data": sosLst})
    else:
        return Response({'message':'Unauthorize Access!!','error':True,'code':401,'result':{'totalItems':0,'items':[],'totalPages':0,'currentPage':0}}, status= status.HTTP_401_UNAUTHORIZED)

@api_view(["POST"])
def getGrivanceByNumber(request, page):    
    data = json.loads(getData(request.data.get("data")))
    print(data)
    try:
        res = list(grievance.objects.filter(primaryNumber = str(data["phoneNumber"])).order_by("-createDate").values())
    except:
        return Response({"message": "No Grivance Found", "error": True, "status": 200}, status=status.HTTP_200_OK)
    paginator = Paginator(res, per_page=20)
    res = list(paginator.get_page(page))
    return Response({"data": res, "count": paginator.count})

#<-------------------------------Found Item------------------------------->#

@api_view(["POST"])
def postFoundItem(request):
    data = getData(request.data.get("data")).decode("utf-8")
    # print(data)
    data = json.loads(data)
    eventName = data.get("eventName")
    language = data.get("language")
    cat = data.get("category")
    data = data.get("data")
    user = request.headers.get("Authorization")
    # print(user)
    # print(data)
    user = jwt.decode(user, verify=False, algorithms=["HS256"], options={"verify_signature": False}) 
    print(user)
    eventId = event.objects.get(eventName = eventName).eventId
    # print(eventId)
    if language == "Odia":
        id = category.objects.get(categoryNameO = cat).categoryId
        bId = beatBox.objects.get(beatBoxDescriptionO = data["beatBoxDescriptionO"]).beatBoxId
        del data["beatBoxDescriptionO"]
    else:
        id = category.objects.get(categoryName = cat).categoryId
        bId = beatBox.objects.get(beatBoxDescription = data["beatBoxDescription"]).beatBoxId
        del data["beatBoxDescription"]
    # print(id)
    data["categoryId"] = id
    data["eventId"] = eventId
    # data["status"] = "Found"
    data["token"] = getID()
    data["modifyDate"] = datetime.now()
    if "lostTokenId" in data and data["lostTokenId"] !="":
        tokenLost = data["lostTokenId"] 
        if tokenLost != "":
            try:
                lost = lostItem.objects.get(token = tokenLost)
            except:
                return Response({"message": "Token doesn't exist", 'error': True}, status=status.HTTP_404_NOT_FOUND)
            print(lost)
            # setattr(lost, "token", tokenLost)
            setattr(lost, "status", data["status"])
            setattr(lost, "beatBoxId", bId)
            lost.save()
        
    # data["delFlag"] = False
    # print(data)
    if user["roleId"] == "1":
        data["uesrId"] = user["userId"]
        data["beatBoxId"] = bId

        # print(data, "1")
        if "image" in data and data["image"] != "":
            for i in range(len(data["image"])):
                image = data["image"][i]
                imageUp = imageStorage.objects.create(eventId = "1", functionName = "found", token = data["token"], image = image, modifyDate = datetime.now())
        
        data["imageURL"] = ""
        # try:
        #     image = data["image"]
        #     print(image)
        #     del data["image"]
        #     img = Image.open(io.BytesIO(base64.decodebytes(bytes(image, "utf-8"))))
        #     img.save("./static/image/found/" + str(data["token"]) + ".png")
        #     # with open("./static/image/found/" + str(data["token"]) + ".png", "wb") as fh:
        #     #     fh.write(base64.decodebytes(image))
        #     data["imageURL"] = "found/" + str(data["token"]) + ".png"
        # except:
        #     data["imageURL"] = ""
        # print(data)
        serializer = foundItemSerializer(data=data)
    # print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message':'Unauthorize Access!!','error':True,'code':401,'result':{'totalItems':0,'items':[],'totalPages':0,'currentPage':0}}, status= status.HTTP_401_UNAUTHORIZED)

@api_view(["GET"])
def getFoundItem(request, page, date):    
    # user = request.headers.get("Authorization")
    language = request.headers.get("language")
    # user = jwt.decode(user, verify=False, algorithms=["HS256"], options={"verify_signature": False}) 
    # if user["roleId"] == "1":
    # print("P")
    foundLst1 = foundItem.objects.all().order_by('-createDate')
    if date != " ":
        import datetime
        foundLst1 = foundLst1.filter(createDate__range = (datetime.datetime.combine(datetime.datetime.strptime(date, "%Y-%m-%d"), datetime.time.min),
                        datetime.datetime.combine(datetime.datetime.strptime(date, "%Y-%m-%d"), datetime.time.max)))
    foundLst1 = foundLst1.values()
    if len(list(foundLst1)) == 0:
        return Response({'data':[],'count': 0})
    paginator = Paginator(foundLst1, per_page=20)
    foundLst = list(paginator.get_page(page))
    # pageC = int(paginator.count / 20)
    # if int(paginator.count % 20) > 0:
    #     pageC += 1
    # if int(page) > pageC:
    #     return Response({'message':'No Data','error':True,'code':404}, status= status.HTTP_404_NOT_FOUND)
    # print(len(list(foundLst)))
    # return Response({"data":list(page_object)})
    # sosLst = (list(list(sosLstP)[0]))
    i = 0
    while i < len(foundLst):
        if foundLst[i]["delFlag"]:
            foundLst.pop(i)
            continue
        elem = foundLst[i]            
        id = elem["eventId"]
        del foundLst[i]["eventId"]
        if not eventCheck(id):
            foundLst.pop(i)
        else:
            # print(i, list(beatBox.objects.filter(beatBoxId = foundLst[i]["beatBoxId"])))
            foundLst[i]["beatBox"] = list(beatBox.objects.filter(beatBoxId = foundLst[i]["beatBoxId"]).values())
            id = elem["categoryId"]
            del foundLst[i]["categoryId"]
            catLs = getCategory(id)
            if language == "Odia":                    
                foundLst[i]["categoryName"] = catLs[1]
                foundLst[i]["categoryType"] = catLs[3]
                foundLst[i]["priority"] = catLs[5]
            else:
                foundLst[i]["categoryName"] = catLs[0]
                foundLst[i]["categoryType"] = catLs[2]
                foundLst[i]["priority"] = catLs[4]
            # print(baseURL,i,foundLst[i]["imageURL"])            
            foundLst[i]["image"] = list(imageStorage.objects.filter(functionName = "found").filter(token = foundLst[i]["token"]).values())
            i += 1                
    
    return Response({"data": foundLst, "count": paginator.count})
    # else:
    #     return Response({'message':'Unauthorize Access!!','error':True,'code':401,'result':{'totalItems':0,'items':[],'totalPages':0,'currentPage':0}}, status= status.HTTP_401_UNAUTHORIZED)
    
@api_view(["GET"])
def getFoundItemById(request, id):    
    user = request.headers.get("Authorization")
    language = request.headers.get("language")
    user = jwt.decode(user, verify=False, algorithms=["HS256"], options={"verify_signature": False}) 
    if user["roleId"] == "1":
        try:
            foundLst = list(foundItem.objects.filter(foundItemId = id).values())[0]
        except:
            return Response({"message": "ID doesn't exist", 'error': True}, status=status.HTTP_404_NOT_FOUND)
        print(list(foundLst))
        id = foundLst["eventId"]
        del foundLst["eventId"]
        id = foundLst["categoryId"]
        del foundLst["categoryId"]
        catLs = getCategory(id)
        if language == "Odia":                    
            # foundLst["categoryName"] = catLs[1]
            # foundLst["categoryType"] = catLs[3]
            # foundLst["priority"] = catLs[5]
            foundLst["beatBoxDescription"] = list(beatBox.objects.filter(beatBoxId = foundLst["beatBoxId"]).values())[0]["beatBoxDescriptionO"]
        else:
            foundLst["beatBoxDescription"] = list(beatBox.objects.filter(beatBoxId = foundLst["beatBoxId"]).values())[0]["beatBoxDescription"]
        foundLst["categoryName"] = catLs[0]
        foundLst["categoryType"] = catLs[2]
        foundLst["priority"] = catLs[4]        
        foundLst["image"] = list(imageStorage.objects.filter(functionName = "found").filter(token = foundLst["token"]).values())
        foundLst["beatBox"] = list(beatBox.objects.filter(beatBoxId = foundLst["beatBoxId"]).values())[0]["beatBoxDescription"]
        return Response({"data": foundLst})
    else:
        return Response({'message':'Unauthorize Access!!','error':True,'code':401,'result':{'totalItems':0,'items':[],'totalPages':0,'currentPage':0}}, status= status.HTTP_401_UNAUTHORIZED)

@api_view(["PUT"])
def hideFoundItemById(request, id):
    user = request.headers.get("Authorization")
    user = jwt.decode(user, verify=False, algorithms=["HS256"], options={"verify_signature": False}) 
    if user["roleId"] == "1":
        try:
            obj = foundItem.objects.filter(foundItemId = id)
        except:
            return Response({"message": "ID doesn't exist", 'error': True}, status=status.HTTP_404_NOT_FOUND)
        obj.update(delFlag = True)
        # obj.save()
        return Response({'message':'Updated Successfully','error':False,'code':200})
    else:
        return Response({'message':'Unauthorize Access!!','error':True,'code':401,'result':{'totalItems':0,'items':[],'totalPages':0,'currentPage':0}}, status= status.HTTP_401_UNAUTHORIZED)

@api_view(["PUT"])
def updateFoundItemById(request):
    user = request.headers.get("Authorization")
    user = jwt.decode(user, verify=False, algorithms=["HS256"], options={"verify_signature": False}) 
    if user["roleId"] == "1":
        data = json.loads(getData(request.data.get("data")))
        id = data.get("id")
        data = data.get("data")
        try:
            obj = foundItem.objects.get(foundItemId = id)
        except:
            return Response({"message": "ID doesn't exist", 'error': True}, status=status.HTTP_404_NOT_FOUND)
        
        id = category.objects.get(categoryName = data["category"]).categoryId
        bId = beatBox.objects.get(beatBoxDescription = data["beatBoxDescription"]).beatBoxId
        del data["beatBoxDescription"]
        data["categoryId"] = id
        data["beatBoxId"] = bId
        print(data)
        if "lostTokenId" in data and data["lostTokenId"] !="":
            print("lost")
            tokenLost = data["lostTokenId"] 
            if tokenLost != "":
                try:
                    lost = lostItem.objects.get(token = tokenLost)
                    setattr(lost, "status", data["status"])
                    setattr(lost, "updatedBy", user["userId"])
                    setattr(lost, "beatBoxId", bId)
                    # print(list(lost))
                    lost.save()
                except:
                    return Response({"message": "Token doesn't exist", 'error': True}, status=status.HTTP_404_NOT_FOUND)
                print(lost)
                # setattr(lost, "token", token)
        keys = list(data.keys())
        for i in range(len(keys)):
            setattr(obj, keys[i], data[keys[i]])
        setattr(lost, "updatedBy", user["userId"])
        obj.save()
        return Response({'message':'Updated Successfully','error':False,'code':200}, status= status.HTTP_200_OK)
    else:
        return Response({'message':'Unauthorize Access!!','error':True,'code':401,'result':{'totalItems':0,'items':[],'totalPages':0,'currentPage':0}}, status= status.HTTP_401_UNAUTHORIZED)

@api_view(["POST"])
def filterFoundItem(request, page):
    data = json.loads(getData(request.data.get("data")))
    # user = request.headers.get("Authorization")
    # user = jwt.decode(user, verify=False, algorithms=["HS256"], options={"verify_signature": False})
    # print(user, type(data))
    # if user["roleId"] == "1":
    obj = ""
    # print(data["categoryId"])
    if data["categoryName"] != "":
        id = category.objects.get(categoryName = data["categoryName"]).categoryId
        obj = foundItem.objects.filter(categoryId = id)
        # print(obj)
    if data["status"] != "":
        if obj == "":
            obj = foundItem.objects.filter(status = data["status"])
        else:
            obj = obj.filter(status = data["status"])
        # print(obj)
    if data["lostToken"] != "":
        if obj == "":
            obj = foundItem.objects.filter(lostTokenId = data["lostToken"])
        else:
            obj = obj.filter(lostTokenId = data["lostToken"])
        # print(obj)
    if "foundToken" in data and data["foundToken"] != "":
        if obj == "":
            obj = foundItem.objects.filter(token = data["foundToken"])
        else:
            obj = obj.filter(token = data["foundToken"])
        # print(obj)
    if "beatBoxId" in data and data["beatBoxId"] != "":
        if obj == "":
            obj = foundItem.objects.filter(beatBoxId = data["beatBoxId"])
        else:
            obj = obj.filter(beatBoxId = data["beatBoxId"])
        print(obj)
    if data["fromDate"] != "":
        print(obj)
        import datetime
        if obj == "":
            # obj = foundItem.objects.filter(createDate = data["createDate"])
            obj = foundItem.objects.filter(createDate__range = (datetime.datetime.combine(datetime.datetime.strptime(data["fromDate"], "%Y-%m-%dT%H:%M"), datetime.time.min),
                        datetime.datetime.combine(datetime.datetime.strptime(data["toDate"], "%Y-%m-%dT%H:%M"), datetime.time.max)))
        else:
            obj = obj.filter(createDate__range = (datetime.datetime.combine(datetime.datetime.strptime(data["fromDate"], "%Y-%m-%dT%H:%M"), datetime.time.min),
                        datetime.datetime.combine(datetime.datetime.strptime(data["toDate"], "%Y-%m-%dT%H:%M"), datetime.time.max)))
    obj = obj.order_by("-createDate").values()
    paginator = Paginator(obj, per_page=20)
    foundLst = list(paginator.get_page(page))
    i = 0
    language = request.headers.get("language")
    while i < len(foundLst):
        if foundLst[i]["delFlag"]:
            foundLst.pop(i)
            continue
        elem = foundLst[i]            
        id = elem["eventId"]
        del foundLst[i]["eventId"]
        if not eventCheck(id):
            foundLst.pop(i)
        else:
            id = elem["categoryId"]
            del foundLst[i]["categoryId"]
            catLs = getCategory(id)
            if language == "Odia":                    
                foundLst[i]["categoryName"] = catLs[1]
                foundLst[i]["categoryType"] = catLs[3]
                foundLst[i]["priority"] = catLs[5]
            else:
                foundLst[i]["categoryName"] = catLs[0]
                foundLst[i]["categoryType"] = catLs[2]
                foundLst[i]["priority"] = catLs[4]
            # print(baseURL,i,foundLst[i]["imageURL"])
            foundLst[i]["image"] = list(imageStorage.objects.filter(functionName = "found").filter(token = foundLst[i]["token"]).values())
            i += 1                
    
    return Response({"data": foundLst, "count": paginator.count})
    # else:
    #     return Response({'message':'Unauthorize Access!!','error':True,'code':401,'result':{'totalItems':0,'items':[],'totalPages':0,'currentPage':0}}, status= status.HTTP_401_UNAUTHORIZED)

#<-------------------------------Lost Item------------------------------->#

@api_view(["POST"])
def postLostItem(request):
    vaildator = getData(request.META["HTTP_VALIDATOR"]).decode("utf-8")
    print(str(vaildator))
    if str(vaildator) != token.postLost():
        return Response({"message": "Validation Fialed", 'error':True,'code':404}, status= status.HTTP_404_NOT_FOUND)
    data = getData(request.data.get("data")).decode("utf-8")
    print(data)
    data = json.loads(data)
    eventName = data.get("eventName")
    language = data.get("language")
    cat = data.get("category")
    data = data.get("data")
    # user = request.headers.get("Authorization")
    # print(user)
    # print(data)
    # user = getRole(user)
    eventId = event.objects.get(eventName = eventName).eventId
    print(eventId)
    if language == "Odia":
        id = category.objects.get(categoryNameO = cat).categoryId
    else:
        id = category.objects.get(categoryName = cat).categoryId
    # print(id)
    data["categoryId"] = id
    data["eventId"] = eventId
    data["status"] = "Open"
    data["token"] = getID()
    data["modifyDate"] = datetime.now()
    # data["delFlag"] = False
    print(data)
    # if user["role"] == "Police":
    # data["uesrId"] = user["userId"]
    # data["beatBoxId"] = bId
    print(data, "1")
    if "image" in data and data["image"] != "":
        for i in range(len(data["image"])):
            image = data["image"][i]
            imageUp = imageStorage.objects.create(eventId = "1", functionName = "lost", token = data["token"], image = image, modifyDate = datetime.now())
        # img = Image.open(io.BytesIO(base64.decodebytes(bytes(image, "utf-8"))))
        # img.save("./static/image/lost/" + str(data["token"]) + ".png")
        # # with open("./static/image/found/" + str(data["token"]) + ".png", "wb") as fh:
        # #     fh.write(base64.decodebytes(image))
        # data["imageURL"] = "lost/" + str(data["token"]) + ".png"
        del data["image"]
    data["imageURL"] = ""
    print(data)
    serializer = lostItemSerializer(data=data)
# print(serializer)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # else:
    #     return Response({'message':'Unauthorize Access!!','error':True,'code':401,'result':{'totalItems':0,'items':[],'totalPages':0,'currentPage':0}}, status= status.HTTP_401_UNAUTHORIZED)

@api_view(["GET"])
def getLostItem(request, page, date):    
    language = request.headers.get("language")
    lostLst1 = lostItem.objects.all().order_by('-createDate')
    if date != " ":
        import datetime
        lostLst1 = lostLst1.filter(createDate__range = (datetime.datetime.combine(datetime.datetime.strptime(date, "%Y-%m-%d"), datetime.time.min),
                        datetime.datetime.combine(datetime.datetime.strptime(date, "%Y-%m-%d"), datetime.time.max)))
    lostLst1 = lostLst1.values()
    if len(list(lostLst1)) == 0:
        return Response({'data':[],'count': 0})
    paginator = Paginator(lostLst1, per_page=20)
    lostLst = list(paginator.get_page(page))
    print(list(lostLst))
    pageC = int(paginator.count / 20)
    # if int(paginator.count % 20) > 0:
    #     pageC += 1
    # if int(page) > pageC:
    #     return Response({'message':'No Data','error':True,'code':404}, status= status.HTTP_404_NOT_FOUND)
    # return Response({"data":list(page_object)})
    # sosLst = (list(list(sosLstP)[0]))
    i = 0
    while i < len(lostLst):
        if lostLst[i]["delFlag"]:
            lostLst.pop(i)
            continue
        elem = lostLst[i]            
        id = elem["eventId"]
        del lostLst[i]["eventId"]
        if not eventCheck(id):
            lostLst.pop(i)
        else:
            id = elem["categoryId"]
            del lostLst[i]["categoryId"]
            catLs = getCategory(id)
            if language == "Odia":                    
                lostLst[i]["categoryName"] = catLs[1]
                lostLst[i]["categoryType"] = catLs[3]
                lostLst[i]["priority"] = catLs[5]
            else:
                lostLst[i]["categoryName"] = catLs[0]
                lostLst[i]["categoryType"] = catLs[2]
                lostLst[i]["priority"] = catLs[4]
            lostLst[i]["image"] = list(imageStorage.objects.filter(functionName = "lost").filter(token = lostLst[i]["token"]).values())
            print(baseURL,i,lostLst[i]["image"])
            # if lostLst[i]["imageURL"] and lostLst[i]["imageURL"] != "":
            #     lostLst[i]["imageURL"] = baseURL + lostLst[i]["imageURL"]
            i += 1                
    
    return Response({"data": lostLst, "count": paginator.count})
    
@api_view(["GET"])
def getLostItemById(request, id):    
    language = request.headers.get("language")
    try:
        lostLst = list(lostItem.objects.filter(lostItemId = id).values())[0]
    except:
        return Response({"message": "ID doesn't exist", 'error': True}, status=status.HTTP_404_NOT_FOUND)
    print(list(lostLst))
    id = lostLst["eventId"]
    del lostLst["eventId"]
    if not eventCheck(id):
        return Response({"message": ""}, status=status.HTTP_400_BAD_REQUEST)
    id = lostLst["categoryId"]
    del lostLst["categoryId"]
    catLs = getCategory(id)
    if language == "Odia":                    
        lostLst["categoryName"] = catLs[1]
        lostLst["categoryType"] = catLs[3]
        lostLst["priority"] = catLs[5]
    else:
        lostLst["categoryName"] = catLs[0]
        lostLst["categoryType"] = catLs[2]
        lostLst["priority"] = catLs[4]
    lostLst["image"] = list(imageStorage.objects.filter(functionName = "lost").filter(token = lostLst["token"]).values())

    return Response({"data": lostLst})

@api_view(["PUT"])
def updateLostItemById(request):
    data = json.loads(getData(request.data.get("data")))
    id = data.get("id")
    data = data.get("data")
    try:
        obj = lostItem.objects.get(lostItemId = id)
    except:
        return Response({"message": "ID doesn't exist", 'error': True}, status=status.HTTP_404_NOT_FOUND)
    keys = list(data.keys())
    for i in range(len(keys)):
        setattr(obj, keys[i], data[keys[i]])
    obj.save()
    return Response({'message':'Updated Successfully','error':False,'code':200}, status= status.HTTP_200_OK)

@api_view(["POST"])
def searchLostItem(request):
    vaildator = getData(request.META["HTTP_VALIDATOR"]).decode("utf-8")
    print(str(vaildator))
    if str(vaildator) != token.searchLost():
        return Response({"message": "Validation Fialed", 'error':True,'code':404}, status= status.HTTP_404_NOT_FOUND)
    language = request.headers.get("language")
    data = json.loads(getData(request.data.get("data")))
    tokenx = data.get("token")
    number = data.get("phoneNumber")
    try:
        obj = list(lostItem.objects.filter(token = tokenx).filter(primaryNumber = number).values())[0]
    except:
        return Response({"message": "Invalid token or number", 'error':True,'code':200}, status= status.HTTP_200_OK)
    print(list(obj))
    print(obj)
    id = obj["eventId"]
    del obj["eventId"]
    id = obj["categoryId"]
    del obj["categoryId"]
    catLs = getCategory(id)
    bb = list(beatBox.objects.filter(beatBoxId = obj["beatBoxId"]).values())
    print(bb)
    obj["beatBox"] = bb
    if language == "Odia":                    
        obj["categoryNameO"] = catLs[1]
        obj["categoryTypeO"] = catLs[3]
        obj["priorityO"] = catLs[5]
        if len(bb)!= 0:
            obj["beatBox"]["beatBoxDescription"] = obj["beatBox"]["beatBoxDescriptionO"]
            obj["beatBox"]["location"] = obj["beatBox"]["locationO"]
    else:
        obj["categoryName"] = catLs[0]
        obj["categoryType"] = catLs[2]
        obj["priority"] = catLs[4]
    
        obj["image"] = list(imageStorage.objects.filter(functionName = "lost").filter(token = obj["token"]).values())

    return Response({"data": obj})

@api_view(["POST"])
def filterLostItem(request, page):
    data = json.loads(getData(request.data.get("data")))
    user = request.headers.get("Authorization")
    user = jwt.decode(user, verify=False, algorithms=["HS256"], options={"verify_signature": False})
    print(user, type(data))
    if user["roleId"] == "1":
        obj = ""
        # print(data["categoryId"])
        if data["categoryName"] != "":
            id = category.objects.get(categoryName = data["categoryName"]).categoryId
            print(id)
            obj = lostItem.objects.filter(categoryId = id)
            print(obj)
        if data["status"] != "":
            if obj == "":
                obj = lostItem.objects.filter(status = data["status"])
            else:
                obj = obj.filter(status = data["status"])
            # print(obj)
        if data["token"] != "":
            if obj == "":
                obj = lostItem.objects.filter(token = data["token"])
            else:
                obj = obj.filter(token = data["token"])
            # print(obj)
        if data["phoneNumber"] != "":
            if obj == "":
                obj = grievance.objects.filter(primaryNumber = str(data["phoneNumber"]))
            else:
                obj = obj.filter(primaryNumber = str(data["phoneNumber"]))
            # print(obj)
        if data["fromDate"] != "":
            import datetime
            if obj == "":
                # obj = foundItem.objects.filter(createDate = data["createDate"])
                obj = lostItem.objects.filter(createDate__range = (datetime.datetime.combine(datetime.datetime.strptime(data["fromDate"], "%Y-%m-%dT%H:%M"), datetime.time.min),
                            datetime.datetime.combine(datetime.datetime.strptime(data["toDate"], "%Y-%m-%dT%H:%M"), datetime.time.max)))
            else:
                obj = obj.filter(createDate__range = (datetime.datetime.combine(datetime.datetime.strptime(data["fromDate"], "%Y-%m-%dT%H:%M"), datetime.time.min),
                            datetime.datetime.combine(datetime.datetime.strptime(data["toDate"], "%Y-%m-%dT%H:%M"), datetime.time.max)))
        obj = obj.order_by("-createDate").values()
        paginator = Paginator(obj, per_page=20)
        lostLst = list(paginator.get_page(page))
        
        i = 0
        language = request.headers.get("language")
        while i < len(lostLst):
            if lostLst[i]["delFlag"]:
                lostLst.pop(i)
                continue
            elem = lostLst[i]            
            id = elem["eventId"]
            del lostLst[i]["eventId"]
            if not eventCheck(id):
                lostLst.pop(i)
            else:
                id = elem["categoryId"]
                del lostLst[i]["categoryId"]
                catLs = getCategory(id)
                if language == "Odia":                    
                    lostLst[i]["categoryName"] = catLs[1]
                    lostLst[i]["categoryType"] = catLs[3]
                    lostLst[i]["priority"] = catLs[5]
                else:
                    lostLst[i]["categoryName"] = catLs[0]
                    lostLst[i]["categoryType"] = catLs[2]
                    lostLst[i]["priority"] = catLs[4]
                # print(baseURL,i,lostLst[i]["imageURL"])
                lostLst[i]["image"] = list(imageStorage.objects.filter(functionName = "lost").filter(token = lostLst[i]["token"]).values())
                i += 1                
    
        return Response({"data": lostLst, "count": paginator.count})
    else:
        return Response({'message':'Unauthorize Access!!','error':True,'code':401,'result':{'totalItems':0,'items':[],'totalPages':0,'currentPage':0}}, status= status.HTTP_401_UNAUTHORIZED)

@api_view(["POST"])
def getLostItemByNumber(request, page):    
    data = json.loads(getData(request.data.get("data")))
    print(data)
    try:
        print(data["phoneNumber"])
        res = list(lostItem.objects.filter(primaryNumber = str(data["phoneNumber"])).order_by("-createDate").values())
        print(res)
        # for i in range(len(res)):
        #     if res[i]["beatBoxId"]!= None:
        #         res[i]["beatBox"] = list(beatBox.objects.filter(beatBoxId = res[i]["beatBoxId"]).values())
        #     else:
        #         res[i]["beatBox"] = []
    except:
        return Response({"message": "No Item Found", "error": True, "status": 200}, status=status.HTTP_200_OK)
    paginator = Paginator(res, per_page=20)
    res = list(paginator.get_page(page))
    for i in range(len(res)):
        if res[i]["beatBoxId"]!= None and res[i]["beatBoxId"]!= "":
            res[i]["beatBox"] = list(beatBox.objects.filter(beatBoxId = res[i]["beatBoxId"]).values())
        else:
            res[i]["beatBox"] = []
    # for i in range(len(res)):
    #     res[i]["beatBox"] = beatBox.objects.filter(res[i]["beatBoxId"])
    return Response({"data": res, "count": paginator.count})

#<-------------------------------Medical Facility------------------------------->#
@api_view(["GET"])
def getMedicalFacility(request, page):
    data = list(medicalFacility.objects.filter(eventId = 1).values())
    language = request.headers.get("language")
    paginator = Paginator(data, per_page=20)
    data = list(paginator.get_page(page))
    i = 0
    while i < len(data):
        # if not eventCheck(data[i]["eventId"]):
        #     data.pop(i)
        # else:
        fac = list(facilities.objects.filter(facilityType = "Medical").filter(facilityTypeId = data[i]["medicalFacilityId"]).values())
        # print(fac)
        data[i]["facilities"] = fac
        if language == "Odia":
            data[i]["name"] = data[i]["nameO"]
            # data[i]["contactNumber"] = data[i]["contactNumberO"]
            data[i]["message"] = data[i]["messageO"]
            data[i]["location"] = data[i]["locationO"]
        print(data)
        data[i]["imageURL"] = baseURL + "facilities/medical/" + str(data[i]["medicalFacilityId"]) + ".jpg"
        i += 1    
    return Response({"data": data, "count": paginator.count})

@api_view(["GET"])
def getMedicalFacilityById(request, id):
    try:
        data = list(medicalFacility.objects.filter(medicalFacilityId = id).values())[0]
    except:
        return Response({"message": "ID doesn't exist", 'error': True}, status=status.HTTP_404_NOT_FOUND)
    if not eventCheck(data["eventId"]):
        return Response({"message": "No Result Found", 'error':True,'code':404}, status= status.HTTP_404_NOT_FOUND)
    fac = list(facilities.objects.filter(facilityType = "Medical").filter(facilityTypeId = id).values())
    # print(fac)
    data["facilities"] = fac
    language = request.headers.get("language")
    if language == "Odia":
        data["name"] = data["nameO"]
        # data["contactNumber"] = data["contactNumberO"]
        data["message"] = data["messageO"]
        data["location"] = data["locationO"]
    data["imageURL"] = baseURL + "facilities/medical/" + str(data["medicalFacilityId"]) + ".jpg"
    return Response({"data": data})

#<-------------------------------Food Distribution------------------------------->#
@api_view(["GET"])
def getFoodDistribution(request, page):
    data = list(foodDistribution.objects.filter(eventId = 1).order_by("foodDistributionId").values())
    language = request.headers.get("language")
    # print(data)
    paginator = Paginator(data, per_page=20)
    data = list(paginator.get_page(page))
    i = 0
    while i < len(data):
        # print(data[i]["foodDistributionId"])
        # if not eventCheck(data[i]["eventId"]):
        #     data.pop(i)
        # else:
        fac = list(facilities.objects.filter(facilityType = "Food Distribution").filter(facilityTypeId = data[i]["foodDistributionId"]).values())
        # print(fac)
        data[i]["facilities"] = fac
        if language == "Odia":
            data[i]["name"] = data[i]["nameO"]
            # data[i]["contactNumber"] = data[i]["contactNumberO"]
            data[i]["message"] = data[i]["messageO"]
            data[i]["location"] = data[i]["locationO"]
        # data[i]["imageURL"] = baseURL + "facilities/foodDistribution/" + str(data[i]["foodDistributionId"]) + ".jpg"
        i += 1
    return Response({"data": data, "count": paginator.count})

@api_view(["POST"])
def filterFoodDistribution(request, page):
    data = request.data
    print(data)
    obj = ""
    if "foodType" in data and data["foodType"] != "":
       obj = foodDistribution.objects.filter(foodType__icontains = data["foodType"])
    if "location" in data and data["location"] != "":
        if obj != "":
            obj = obj.filter(location = data["location"])
        else:
            obj = foodDistribution.objects.filter(location = data["location"])
    if "date" in data and data["date"] != "":
        if obj != "":
            obj = obj.filter(preferedDate = (datetime.strptime(data["date"], "%Y-%m-%d")))
        else:
            obj = foodDistribution.objects.filter(preferedDate = (datetime.strptime(data["date"], "%Y-%m-%d")))
    obj = list(obj.order_by("foodDistributionId").values())
    language = request.headers.get("language")
    # print(data)
    paginator = Paginator(obj, per_page=20)
    data = list(paginator.get_page(page))
    if language == "Odia":
        for i in range(len(data)):
            data[i]["name"] = data[i]["nameO"]
            data[i]["location"] = data[i]["locationO"]
            data[i]["message"] = data[i]["messageO"]
            data[i]["foodType"] = data[i]["foodTypeO"]
    return Response({"data": data, "count": paginator.count})

# @api_view(["POST"])
# def foodDistributionByDate(request, page):
#     data = request.data
#     print(data)
#     # data = list(foodDistribution.objects.filter(eventId = 1).order_by("foodDistributionId").values())
#     obj = list(foodDistribution.objects.filter(preferedDate = (datetime.strptime(data["date"], "%Y-%m-%d"))).values())
#     language = request.headers.get("language")
#     # print(data)
#     paginator = Paginator(obj, per_page=20)
#     data = list(paginator.get_page(page))
#     if language == "Odia":
#         for i in range(len(data)):
#             data[i]["name"] = data[i]["nameO"]
#             data[i]["location"] = data[i]["locationO"]
#             data[i]["message"] = data[i]["messageO"]
#             data[i]["foodType"] = data[i]["foodTypeO"]
#     return Response({"data": data})

@api_view(["GET"])
def getFoodDistributionById(request, id):
    try:
        data = list(foodDistribution.objects.filter(foodDistributionId = id).values())[0]
    except:
        return Response({"message": "ID doesn't exist", 'error': True}, status=status.HTTP_404_NOT_FOUND)
    if not eventCheck(data["eventId"]):
        return Response({"message": "No Result Found", 'error':True,'code':404}, status= status.HTTP_404_NOT_FOUND)
    fac = list(facilities.objects.filter(facilityType = "Food Distribution").filter(facilityTypeId = data["foodDistributionId"]).values())
            # print(fac)
    data["facilities"] = fac
    language = request.headers.get("language")
    if language == "Odia":
        data["name"] = data["nameO"]
        # data["contactNumber"] = data["contactNumberO"]
        data["message"] = data["messageO"]
        data["location"] = data["locationO"]
    data["imageURL"] = baseURL + "facilities/foodDistribution/" + str(data["foodDistributionId"]) + ".jpg"
    return Response({"data": data})

#<-------------------------------Washroom------------------------------->#
@api_view(["GET"])
def getWashroom(request, page):
    data = list(washroom.objects.filter(eventId = 1).values())
    language = request.headers.get("language")
    paginator = Paginator(data, per_page=20)
    data = list(paginator.get_page(page))
    i = 0
    while i < len(data):
        # if not eventCheck(data[i]["eventId"]):
        #     data.pop(i)
        # else:
        fac = list(facilities.objects.filter(facilityType = "Washroom").filter(facilityTypeId = data[i]["washroomId"]).values())
        # print(fac)
        data[i]["facilities"] = fac
        if language == "Odia":
            data[i]["name"] = data[i]["nameO"]
            # data[i]["contactNumber"] = data[i]["contactNumberO"]
            data[i]["message"] = data[i]["messageO"]
            data[i]["location"] = data[i]["locationO"]
        data[i]["imageURL"] = baseURL + "facilities/washroom/" + str(data[i]["washroomId"]) + ".jpg"
        i += 1
    return Response({"data": data, "count": paginator.count})

#<-------------------------------Shoe Stand------------------------------->#
@api_view(["GET"])
def getShoeStand(request, page):
    data = list(shoeStand.objects.filter(eventId = 1).values())
    language = request.headers.get("language")
    paginator = Paginator(data, per_page=20)
    data = list(paginator.get_page(page))
    i = 0
    while i < len(data):
        # if not eventCheck(data[i]["eventId"]):
        #     data.pop(i)
        # else:
        if language == "Odia":
            data[i]["name"] = data[i]["nameO"]
            # data[i]["contactNumber"] = data[i]["contactNumberO"]
            data[i]["message"] = data[i]["messageO"]
            data[i]["location"] = data[i]["locationO"]
        data[i]["imageURL"] = baseURL + "facilities/shoeStand/" + str(data[i]["shoeStandId"]) + ".jpg"
        i += 1
    return Response({"data": data, "count": paginator.count})

#<-------------------------------Day wise Ritual------------------------------>#

@api_view(["GET"])
def getDayWiseRituals(request):
    data = dayWiseRitual.objects.all().order_by("dayWiseRitualId").values()
    language = request.headers.get("language")
    i = 0
    while i < len(data):
        if not eventCheck(data[i]["eventId"]) or data[i]["delFlag"]:
            data.pop(i)
        else:
            if language == "Odia":
                data[i]["ritualName"] = data[i]["ritualNameO"]
            i += 1
    return Response({"data": data})

@api_view(["GET"])
def getRitualsById(request, id):
    language = request.headers.get("language")
    try:
        data = list(timeWiseRitual.objects.filter(dayWiseRitualId = id).values())
    except:
        return Response({"message": "ID doesn't have time wise ritual", 'error': True}, status=status.HTTP_404_NOT_FOUND)
    i = 0
    while i < len(data):
        if not eventCheck(data[i]["eventId"]) or data[i]["delFlag"]:
            data.pop(i)
        else:
            res =  list(dayWiseRitual.objects.filter(dayWiseRitualId = data[i]["dayWiseRitualId"]).values())[0]
            if language == "Odia":
                data[i]["ritualName"] = data[i]["ritualNameO"]
                dayWiseRitualName = res["ritualNameO"]
            else:
                dayWiseRitualName = res["ritualName"]
            i += 1
    return Response({"dayWiseRitualName": dayWiseRitualName,"data": data})

@api_view(["GET"])
def getFaclities(request):
    return Response(facilities.objects.all().values())

#<-------------------------------Hotel------------------------------>#

@api_view(["GET"])
def getHotels(request, page):
    starRatings = ["1 Star","2 Star","3 Star","4 Star","5 Star","LSG", "HSG", "MSG"]
    data = hotels.objects.filter(eventId = 1)
    print(data.count())
    stars = {}
    for st in starRatings:
        temp = data.filter(starRating = st).count()
        if temp != 0:
            stars[st] = temp
    data = list(data.values())
    paginator = Paginator(data, per_page=20)
    data = list(paginator.get_page(page))
    return Response({"data": data, "count": paginator.count, "starCount": stars})

@api_view(["POST"])
def filterHotel(request, page):
    starRatings = request.data.get("filter")
    data = hotels.objects.filter(eventId = 1)
    res =  []   
    for st in starRatings:
        res += list(data.filter(starRating = st).values())    
    paginator = Paginator(res, per_page=20)
    data = list(paginator.get_page(page))
    return Response({"data": data, "count": paginator.count})
    

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
@api_view(["POST"])
def postHotel(request):
    data = request.data
    print(data)
    # data = json.loads(data)
    data["modifyDate"] = datetime.now()
    print(data, "1")
    serializer = hotelSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def deleteHotel(request):
    id = request.data.get("id")
    res = hotels.objects.filter(hotelId = id).delete()
    return Response(res)
#<-------------------------------Water------------------------------>#

@api_view(["GET"])
def getWaterSpots(request, page):
    data = waterSpots.objects.filter(eventId = 1).values()
    language = request.headers.get("language")
    paginator = Paginator(data, per_page=20)
    data = list(paginator.get_page(page))
    i = 0
    while i < len(data):
        # if not eventCheck(data[i]["eventId"]) or data[i]["delFlag"]:
        #     data.pop(i)
        # else:
        if language == "Odia":
            data[i]["name"] = data[i]["nameO"]
            data[i]["location"] = data[i]["locationO"]
            data[i]["message"] = data[i]["messageO"]
        i += 1
    return Response({"data": data, "count": paginator.count})

# # #generate random string

# def getID():
#     d = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')[:-3]
#     id = abs(hash(d)) % (10 ** 8)
#     return id

# # def saveImage(token, image, lost_found):
# #     AZURE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=rathyatrastorage;AccountKey=Q0V+sjgzHsJRvmP7DVh49qlANpcFd4W2nQwE6sZw8DrTrcmxc6pIkvYKphURzNd1XxKJpamrGtUu+AStT6ezSQ==;EndpointSuffix=core.windows.net"
# #     finalImage = base64.b64decode(image)     
# #     imageName = token + ".png"
# #     print(lost_found)
# #     blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
# #     container_client = blob_service_client.get_container_client(lost_found)
# #     blob_client = container_client.get_blob_client(imageName)
# #     blob_client.upload_blob(finalImage, blob_type="BlockBlob")
# #     return imageName


# # # Create your views here.
# # def getCategoryById(id):
# #     data = Category.objects.get(id = id)
# #     #print(id, data.CategoryName)
# #     return data.categoryName

# # def getBeatBoxById(id):
# #     data = Beat_box.objects.get(id = id)
# #     #print(data.Details)
# #     return data.details


# # #<----------------------------------------Login---------------------------------------->#
# # @api_view(["POST"])
# # def login(request):
# #     user = request.data.get("user")
# #     password = request.data.get("password")

# #     pass

# # #<----------------------------------------Parking---------------------------------------->#
# # @api_view(["GET"])
# # def getParkingDetails(request):
# #     data = Parking.objects.all().values()
# #     return Response({"data": data})

# # @api_view(["GET"])
# # def getParkingDetailById(request,id):
# #     data = list(Parking.objects.filter(ID = id).values())
# #     return Response({"data": data})

# # @api_view(["PUT"])
# # def updateParkingById(request):
# #     id = request.data.get("id")
# #     print(id)
# #     data = request.data.get("data")
# #     print(data)
# #     obj = Parking.objects.get(ID = id)
# #     keys = list(data.keys())
# #     for i in range(len(keys)):
# #         setattr(obj, keys[i], data[keys[i]])
# #     obj.save()
# #     return HttpResponse("Updated Successfully!")
# #     # Parking.objects.filter(ID = id).update(vaccancy = vaccancy)
# #     # return HttpResponse("Successful!")


# # #<----------------------------------------Lost Items---------------------------------------->#
# # @api_view(["GET"])
# # def getLostItems(request):
# #     data = list(Lost_and_found.objects.filter(classification = 1).values())
# #     #print(len(data))
# #     for i in range(len(data)):
# #         if  data[i]["hideItem"] == False:
# #             #print(i)
# #             data[i]["category"] = getCategoryById(data[i]["category_id"])
# #             #print(len(data))
# #             data[i]["beatBox"] = getBeatBoxById(data[i]["beatBox_id"])
# #             #print(data)
# #             del data[i]["category_id"]
# #             del data[i]["beatBox_id"]
# #         else:
# #             data.pop(i)
       
# #     return Response({"data": data})

# # @api_view(["GET"])
# # def getLostItemsById(request, id):
# #     data = list(Lost_and_found.objects.filter(ID = id).values())
# #     for i in range(len(data)):
# #         #print(i)
# #         data[i]["category"] = getCategoryById(data[i]["category_id"])
# #         #print(len(data))
# #         data[i]["beatBox"] = getBeatBoxById(data[i]["beatBox_id"])
# #         #print(data)
# #         del data[i]["category_id"]
# #         del data[i]["beatBox_id"]
# #     return Response({"data": data})

# # @api_view(["POST"])
# # def postLostItems(request):
# #     ID = str(getID())
# #     print(request.data, 1)
# #     data = request.data
# #     print(data)
# #     try:
# #         data["imageURL"] = "https://rathyatrastorage.blob.core.windows.net/lostimage/" + saveImage(ID, request.data.get("image"), "lostimage")
# #     except:
# #         data["imageURL"] = "No image"
# #     data["ID"] = ID
# #     del data["image"]
# #     category = list(Category.objects.filter(categoryName = data.get("category")))
# #     #print(d,"d")
# #     #CategoryId = (d[0].id)
# #     data["category"] = category[0].id
# #     data["dateTime"] = datetime.now()
# #     data["classification"] = 1
# #     data["status"] = 1 
# #     data["hideItem"] = False
# #     #beatBox = list(Beat_box.objects.filter(details = data.get("beatBox")))
# #     data["beatBox"] = "1"
# #     cols = colsReq.getLostAndFound()
# #     colsEx = ["latitude", "longitude"]
# #     for col in cols:
# #         if col not in data:
# #             if col in colsEx:
# #                 data[col] = 0.00
# #             else:
# #                 data[col] = "None"
# #     serializer = Lost_and_FoundSerializers(data=data)
# #     if serializer.is_valid():
# #         serializer.save()
# #         return Response(serializer.data, status=status.HTTP_200_OK)

# #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # @api_view(["PUT"])
# # def hideLostItemsById(request):
# #     id = request.data.get("id")
# #     data = Lost_and_found.objects.get(ID = id)
# #     #print(data)
# #     data.hideItem = True
# #     #print(data)
# #     data.save()
# #     return HttpResponse("Updated Successfully!")

# # @api_view(["PUT"])
# # def updateLostItemsById(request):
# #     id = request.data.get("id")
# #     data = request.data.get("data")
# #     obj = Lost_and_found.objects.get(ID = id)
# #     keys = list(data.keys())
# #     for i in range(len(keys)):
# #         setattr(obj, keys[i], data[keys[i]])
# #     obj.save()
# #     return HttpResponse("Updated Successfully!")

# # @api_view(['GET'])
# # def searchLostTokenPhoneNumber(request, data):
# #     if len(str(data)) <= 8:
# #         res = Lost_and_found.objects.filter(ID = data).values()
# #     else:
# #         res = Lost_and_found.objects.filter(primaryPhoneNumber = data).values()
# #     print(res)
# #     data = list(res)
# #     print("1",data)
# #     # print(data,res)
# #     for i in range(len(data)):
# #         #print(i)
# #         data[i]["category"] = getCategoryById(data[i]["category_id"])
# #         #print(len(data))
# #         data[i]["beatBox"] = getBeatBoxById(data[i]["beatBox_id"])
# #         #print(data)
# #         del data[i]["category_id"]
# #         del data[i]["beatBox_id"]
# #     print("2", data[0])
# #     return Response({"data": data[0]})
# # #<----------------------------------------Found Items---------------------------------------->#
# # @api_view(["GET"])
# # def getFoundItems(request):
# #     data = list(Lost_and_found.objects.filter(classification = 2 ).values())
# #     for i in range(len(data)):
# #         if  data[i]["hideItem"] == False:
# #             #print(i)
# #             data[i]["category"] = getCategoryById(data[i]["category_id"])
# #             #print(len(data))
# #             data[i]["beatBox"] = getBeatBoxById(data[i]["beatBox_id"])
# #             #print(data)
# #             del data[i]["category_id"]
# #             del data[i]["beatBox_id"]
# #         else:
# #             data.pop(i)
# #     return Response({"data": data})

# # @api_view(["GET"])
# # def getFoundItemById(request, id): 
# #     data = list(Lost_and_found.objects.filter(ID = id).values())
# #     for i in range(len(data)):
# #         #print(i)
# #         data[i]["category"] = getCategoryById(data[i]["category_id"])
# #         #print(len(data))
# #         data[i]["beatBox"] = getBeatBoxById(data[i]["beatBox_id"])
# #         #print(data)
# #         del data[i]["category_id"]
# #         del data[i]["beatBox_id"]
# #     return Response({"data": data})

# # @api_view(["POST"])
# # def postFoundItems(request):
# #     ID = str(getID())    
# #     print(request.data, 1)
# #     data = request.data
# #     print(data)
# #     data = request.data
# #     data["imageURL"] = "https://rathyatrastorage.blob.core.windows.net/lostimage/" + saveImage(ID, request.data.get("image"), "foundimage")
# #     data["ID"] = ID
# #     del data["image"]
# #     category = list(Category.objects.filter(categoryName = data.get("category")))
# #     #print(d,"d")
# #     #CategoryId = (d[0].id)
# #     data["category"] = category[0].id
# #     data["dateTime"] = datetime.now()
# #     data["classification"] = 2
# #     data["status"] = 1 
# #     data["hideItem"] = False
# #     # beatBox = list(Beat_box.objects.filter(details = data.get("beatBox")))
# #     data["beatBox"] = 1
# #     cols = colsReq.getLostAndFound()
# #     colsEx = ["latitude", "longitude"]
# #     for col in cols:
# #         if col not in data:
# #             if col in colsEx:
# #                 data[col] = 0.00
# #             else:
# #                 data[col] = "None"
# #     serializer = Lost_and_FoundSerializers(data=data)
# #     if serializer.is_valid():
# #         serializer.save()
# #         return Response(serializer.data, status=status.HTTP_200_OK)

# #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # @api_view(["PUT"])
# # def hideFoundItemsById(request):
# #     id = request.data.get("id")
# #     data = Lost_and_found.objects.get(ID = id)
# #     data.hideItem = True
# #     data.save()
# #     return HttpResponse("Updated Successfully!")

# # @api_view(["PUT"])
# # def updateFoundItemsById(request):
# #     id = request.data.get("id")
# #     data = request.data.get("data")
# #     obj = Lost_and_found.objects.get(ID = id)
# #     keys = list(data.keys())
# #     for i in range(len(keys)):
# #         setattr(obj, keys[i], data[keys[i]])
# #     obj.save()
# #     return HttpResponse("Updated Successfully!")