from django.db import models
from datetime import datetime
from django.contrib.postgres.fields import ArrayField
# # # #from phonenumber_field.modelfields import PhoneNumberField
# # # # Create your models here.
# # # class Category(models.Model):
# # #     categoryId = models.CharField(max_length = 255)
# # #     categoryName = models.CharField(max_length = 255)

# # # class Beat_box(models.Model):
# # #     beatBoxId = models.CharField(max_length = 255)
# # #     details  = models.CharField(max_length = 255)

# # # #<----------------------user---------------------->#
# # # class Role(models.Model):
# # #     roleId = models.CharField(max_length = 255)
# # #     roleName = models.CharField(max_length = 255)

# # # class User(models.Model):
# # #     ID = models.CharField(primary_key = True, max_length = 255)
# # #     firstName = models.CharField(max_length = 255)
# # #     lastName = models.CharField(max_length = 255)
# # #     roleId = models.ForeignKey(Role, on_delete = models.CASCADE)
# # #     userName = models.CharField(max_length = 255, unique = True)
# # #     password = models.CharField(max_length = 255)

# # # #<----------------------Lost and Found---------------------->#
# # # class Lost_and_found(models.Model):
# # #     ID = models.CharField(max_length = 255, primary_key = True)
# # #     category = models.ForeignKey(Category, on_delete = models.CASCADE)
# # #     dateTime = models.DateTimeField()
# # #     imageURL = models.CharField(max_length = 255)
# # #     description = models.CharField(max_length = 255)
# # #     name = models.CharField(max_length = 255)
# # #     primaryPhoneNumber = models.CharField(max_length = 13)
# # #     alternatePhoneNumber = models.CharField(max_length = 13)
# # #     latitude = models.DecimalField(max_digits = 20, decimal_places = 10)
# # #     longitude = models.DecimalField(max_digits = 20, decimal_places = 10)
# # #     location = models.CharField(max_length = 255)
# # #     classification = models.IntegerField()
# # #     status = models.IntegerField()
# # #     beatBox = models.ForeignKey(Beat_box, on_delete = models.CASCADE)
# # #     hideItem = models.BooleanField()
    
# # # #<----------------------Parking---------------------->#
# # # class Parking(models.Model):
# # #     ID = models.CharField(max_length = 255, primary_key = True)
# # #     dateTime = models.DateTimeField()
# # #     parkingNumber = models.CharField(max_length = 255)
# # #     capacity = models.BigIntegerField()
# # #     vaccancy = models.BigIntegerField()
# # #     latitude = models.DecimalField(max_digits = 20, decimal_places = 10)
# # #     longitude = models.DecimalField(max_digits = 20, decimal_places = 10)
# # #     location = models.CharField(max_length = 255, null= True)


# # #<----------------New DB---------------->#
class event(models.Model):
    eventId = models.AutoField(primary_key = True)
    eventName = models.CharField(max_length = 255)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    activeFlag = models.BooleanField()
    createDate = models.DateTimeField(auto_now_add = True)
    modifyDate = models.DateTimeField(auto_now = False)

class role(models.Model):
    roleId = models.AutoField(primary_key = True)
    eventId = models.CharField(max_length = 255) # from event table
    roleName = models.CharField(max_length = 255)
    createDate = models.DateTimeField(auto_now_add = True)
    modifyDate = models.DateTimeField(auto_now = False)
    delFlag = models.BooleanField(default = False)

class user(models.Model):
    userId = models.AutoField( primary_key=True)
    eventId = models.CharField(max_length = 255) #from event table
    userName = models.CharField(max_length = 255, null = True, blank = True)
    firstName = models.CharField(max_length = 255)
    lastName = models.CharField(max_length = 255)
    contactNumber = models.CharField(max_length = 255, null = True, blank = True)
    emailId = models.CharField(max_length = 255, null = True, blank = True)
    emergencyContactNumber = models.CharField(max_length = 255, null = True, blank = True)
    password = models.CharField(max_length = 255)
    roleId = models.CharField(max_length = 255) # from role table
    newUser = models.BooleanField(default = True)
    createDate = models.DateTimeField(auto_now_add = True)
    modifyDate = models.DateTimeField(auto_now = False)
    delFlag = models.BooleanField(default = False)

class category(models.Model):
    categoryId = models.AutoField(primary_key = True)
    eventId = models.CharField(max_length = 255) #from event table
    categoryType = models.CharField(max_length = 255)
    categoryTypeO = models.CharField(max_length = 255)
    categoryName = models.CharField(max_length = 255)
    categoryNameO = models.CharField(max_length = 255)
    priority = models.CharField(max_length = 255)
    priorityO = models.CharField(max_length = 255)
    createDate = models.DateTimeField(auto_now_add = True)
    modifyDate = models.DateTimeField(auto_now = False)
    delFlag = models.BooleanField(default = False)

class beatBox(models.Model):
    beatBoxId = models.IntegerField( primary_key = True)
    eventId = models.CharField(max_length = 255) #from event table
    beatBoxDescription = models.CharField(max_length = 1000)
    beatBoxDescriptionO = models.CharField(max_length = 1000)
    openingTime = models.TimeField()
    openingTimeO = models.TimeField()
    closingTime = models.TimeField()
    closingTimeO = models.TimeField()
    location = models.CharField(max_length = 255)
    locationO = models.CharField(max_length = 255)
    latitude = models.DecimalField(max_digits = 10, decimal_places = 8)
    longitude = models.DecimalField(max_digits = 10, decimal_places = 8)    
    createDate = models.DateTimeField(auto_now_add = True)
    modifyDate = models.DateTimeField(auto_now = False)
    delFlag = models.BooleanField(default = False)

class imageStorage(models.Model):    
    imageId = models.AutoField(primary_key = True)
    eventId = models.CharField(max_length = 255) # from event table
    functionName = models.CharField(max_length = 255)
    token = models.CharField(max_length = 255)
    image = models.TextField()
    # image = ArrayField(base_field=models.ImageField())
    createDate = models.DateTimeField(auto_now_add = True)
    modifyDate = models.DateTimeField(auto_now = False)
    delFlag = models.BooleanField(default = False)

class grievance(models.Model):
    grievanceId = models.AutoField( primary_key = True)
    eventId = models.CharField(max_length = 255) #from event table
    location = models.CharField(max_length = 255, null=True, blank=True)
    latitude = models.DecimalField(max_digits = 10, decimal_places = 8, null=True, blank=True)
    longitude = models.DecimalField(max_digits = 10, decimal_places = 8, null=True, blank=True)
    categoryId = models.CharField(max_length = 255) #from category table
    description = models.CharField(max_length = 1000, null = True, blank = True)
    name = models.CharField(max_length = 255, null=True, blank=True)
    primaryNumber = models.CharField(max_length = 255, null=True, blank=True)
    alternateNumber = models.CharField(max_length = 255, null=True, blank=True)
    comments = models.CharField(max_length = 1000, null=True, blank=True)
    updatedBy = models.CharField(max_length = 1000, null=True, blank=True)
    token = models.CharField(max_length = 255)
    status = models.CharField(max_length = 255)
    occuranceDateTime = models.DateTimeField(null=True, blank=True)
    createDate = models.DateTimeField(auto_now_add = True)
    modifyDate = models.DateTimeField(auto_now = False)
    delFlag = models.BooleanField(default = False)

class lostItem(models.Model):
    lostItemId = models.AutoField(primary_key = True)
    eventId = models.CharField(max_length = 255) #from event table
    categoryId = models.CharField(max_length = 255) #from category table
    imageURL = models.CharField(max_length = 255, null=True, blank=True)
    description = models.CharField(max_length = 1000, blank = True, null = True)
    name = models.CharField(max_length = 255, null=True, blank=True)
    primaryNumber = models.CharField(max_length = 255, null=True, blank=True)
    alternateNumber = models.CharField(max_length = 255, null=True, blank=True)
    location = models.CharField(max_length = 255, null=True, blank=True)
    latitude = models.DecimalField(max_digits = 10, decimal_places = 8, null=True, blank=True)
    longitude = models.DecimalField(max_digits = 10, decimal_places = 8, null=True, blank=True)
    foundLocation  = models.CharField(max_length = 255, null = True, blank = True)
    beatBoxId  = models.CharField(max_length = 255, null = True, blank = True)
    token = models.CharField(max_length = 255)
    updatedBy = models.CharField(max_length = 1000, null=True, blank=True)
    status = models.CharField(max_length = 255)
    lostDateTime = models.DateTimeField(null=True, blank=True)
    createDate = models.DateTimeField(auto_now_add = True)
    modifyDate = models.DateTimeField(auto_now = False)
    delFlag = models.BooleanField(default = False)
    
class foundItem(models.Model):
    foundItemId = models.AutoField(primary_key = True)
    eventId = models.CharField(max_length = 255) # from even table
    uesrId = models.CharField(max_length = 255) #from user table
    categoryId = models.CharField(max_length = 255) #from category table
    lostTokenId = models.CharField(max_length = 255, null=True, blank=True)
    imageURL = models.CharField(max_length = 255, null=True, blank=True)
    description = models.CharField(max_length = 1000, blank = True, null = True)
    name = models.CharField(max_length = 255, null=True, blank=True)
    location = models.CharField(max_length = 255, null=True, blank=True)
    latitude = models.DecimalField(max_digits = 10, decimal_places = 8, null=True, blank=True)
    longitude = models.DecimalField(max_digits = 10, decimal_places = 8, null=True, blank=True)
    token = models.CharField(max_length = 255)
    beatBoxId = models.CharField(max_length = 255) # from beat box table
    status = models.CharField(max_length = 255)
    updatedBy = models.CharField(max_length = 1000, null=True, blank=True)
    foundDateTime = models.DateTimeField(null=True, blank=True)
    createDate = models.DateTimeField(auto_now_add = True)
    modifyDate = models.DateTimeField(auto_now = False)
    delFlag = models.BooleanField(default = False)
   
class vehicleType(models.Model):
    vehicleTypeId = models.AutoField(primary_key = True)
    eventId = models.CharField(max_length = 255) # from event table
    vehicleType = models.CharField(max_length = 255)
    createDate = models.DateTimeField(auto_now_add = True)
    modifyDate = models.DateTimeField(auto_now = False)
    delFlag = models.BooleanField(default = False)

class parking_user_X(models.Model):
    parkingXuser = models.AutoField(primary_key = True)
    eventId = models.CharField(max_length = 255) # from event table
    parkingId = models.CharField(max_length = 255)
    userId = models.CharField(max_length = 255)
    createDate = models.DateTimeField(auto_now_add = True)
    modifyDate = models.DateTimeField(auto_now = True)
    delFlag = models.BooleanField(default = False)

class parking(models.Model):
    parkingId = models.CharField(max_length = 255)
    eventId = models.CharField(max_length = 255) # from event table
    userId = models.CharField(max_length = 255, null=True, blank=True) #from user table
    activeFlag = models.BooleanField()
    parkingName = models.CharField(max_length = 255)
    parkingNameO = models.CharField(max_length = 255)
    openingTime = models.TimeField()
    openingTimeO = models.TimeField()
    closingTime = models.TimeField()
    closingTimeO = models.TimeField()
    location = models.CharField(max_length = 255)
    locationO = models.CharField(max_length = 255)
    latitude = models.DecimalField(max_digits = 10, decimal_places = 8)
    longitude = models.DecimalField(max_digits = 10, decimal_places = 8)
    vehicleTypeId = models.CharField(max_length = 255) #from vehicle type table
    capacity = models.IntegerField()
    capacityO = models.IntegerField()
    vacancy = models.IntegerField()
    vacancyO = models.IntegerField()
    charge = models.IntegerField()
    chargeO = models.IntegerField()
    createDate = models.DateTimeField(auto_now_add = True)
    modifyDate = models.DateTimeField(auto_now = False)
    delFlag = models.BooleanField(default = False)

class parkingTransaction(models.Model):
    parkingTransactionId = models.AutoField(primary_key = True)
    eventId = models.CharField(max_length = 255) #from event table
    createDate = models.DateTimeField(auto_now_add = True)
    parkingId = models.CharField(max_length = 255)
    vehicleTypeId = models.CharField(max_length = 255)# from vehicle type table
    out = models.BooleanField(default = True)

class facilities(models.Model):
    facilityId = models.AutoField(primary_key = True)
    eventId = models.CharField(max_length = 255) #from event table
    facilityType = models.CharField(max_length = 255)
    facilityTypeId = models.IntegerField()
    facilityName = models.CharField(max_length = 255)
    facilityLogoId = models.CharField(max_length=20, null=True, blank=True)
    createDate = models.DateTimeField(auto_now_add = True)
    modifyDate = models.DateTimeField(auto_now = False)
    delFlag = models.BooleanField(default = False)

class medicalFacility(models.Model):
    medicalFacilityId = models.AutoField(primary_key = True)
    eventId = models.CharField(max_length = 255) #from event table
    name = models.CharField(max_length = 255)
    nameO =models.CharField(max_length = 255)
    openingTime = models.TimeField()
    openingTimeO = models.TimeField()
    closingTime = models.TimeField()
    closingTimeO = models.TimeField()
    contactNumber = models.CharField(max_length = 255)
    contactNumberO = models.CharField(max_length = 255)
    message = models.CharField(max_length = 255)
    messageO = models.CharField(max_length = 255)    
    location = models.CharField(max_length = 255)
    locationO = models.CharField(max_length = 255)
    latitude = models.DecimalField(max_digits = 10, decimal_places = 8)
    longitude = models.DecimalField(max_digits = 10, decimal_places = 8)
    createDate = models.DateTimeField(auto_now_add = True)
    modifyDate = models.DateTimeField(auto_now = False)
    delFlag = models.BooleanField(default = False)

class foodDistribution(models.Model):
    foodDistributionId = models.AutoField(primary_key = True)
    eventId = models.CharField(max_length = 255) #from event table
    name = models.CharField(max_length = 255, null = True, blank = True)
    nameO =models.CharField(max_length = 255, null = True, blank = True)   
    location = models.CharField(max_length = 255)
    locationO = models.CharField(max_length = 255)
    latitude = models.DecimalField(max_digits = 10, decimal_places = 8)
    longitude = models.DecimalField(max_digits = 10, decimal_places = 8)
    message = models.CharField(max_length = 255)
    messageO = models.CharField(max_length = 255)       
    openingTime = models.TimeField()
    openingTimeO = models.TimeField()
    closingTime = models.TimeField()
    closingTimeO = models.TimeField()
    contactNumber = models.CharField(max_length = 255)
    contactNumberO = models.CharField(max_length = 255)
    menuLink = models.URLField(max_length = 255)
    preferedDate = models.DateField(null=True, blank=True)
    foodType = models.CharField(max_length = 255, null = True, blank = True)
    foodTypeO = models.CharField(max_length = 255, null = True, blank = True)
    numberOfBeneficiary = models.IntegerField(null = True, blank = True)
    # cuisine = models.CharField(max_length = 255)
    # cuisineO = models.CharField(max_length = 255)
    createDate = models.DateTimeField(auto_now_add = True)
    modifyDate = models.DateTimeField(auto_now = False)
    delFlag = models.BooleanField(default = False)

class washroom(models.Model):
    washroomId = models.AutoField(primary_key = True)
    eventId = models.CharField(max_length = 255) #from event table
    name = models.CharField(max_length = 255)
    nameO =models.CharField(max_length = 255)   
    location = models.CharField(max_length = 255)
    locationO = models.CharField(max_length = 255)
    latitude = models.DecimalField(max_digits = 10, decimal_places = 8)
    longitude = models.DecimalField(max_digits = 10, decimal_places = 8)
    openingTime = models.TimeField()
    openingTimeO = models.TimeField()
    closingTime = models.TimeField()
    closingTimeO = models.TimeField()
    message = models.CharField(max_length = 255)
    messageO = models.CharField(max_length = 255)
    paid = models.BooleanField()
    charge = models.CharField(max_length = 255, null=True, blank=True)    
    chargeO = models.CharField(max_length = 255, null=True, blank=True)
    createDate = models.DateTimeField(auto_now_add = True)
    modifyDate = models.DateTimeField(auto_now = False)
    delFlag = models.BooleanField(default = False)

class shoeStand(models.Model):
    shoeStandId = models.AutoField(primary_key = True)
    eventId = models.CharField(max_length = 255) #from event table
    name = models.CharField(max_length = 255)
    nameO =models.CharField(max_length = 255)   
    location = models.CharField(max_length = 255)
    locationO = models.CharField(max_length = 255)
    latitude = models.DecimalField(max_digits = 10, decimal_places = 8)
    longitude = models.DecimalField(max_digits = 10, decimal_places = 8)
    openingTime = models.TimeField()
    openingTimeO = models.TimeField()
    closingTime = models.TimeField()
    closingTimeO = models.TimeField()
    message = models.CharField(max_length = 255)
    messageO = models.CharField(max_length = 255)
    paid = models.BooleanField()
    charge = models.CharField(max_length = 255, null=True, blank=True)
    chargeO = models.CharField(max_length = 255, null=True, blank=True)
    mobileStore = models.BooleanField()
    createDate = models.DateTimeField(auto_now_add = True)
    modifyDate = models.DateTimeField(auto_now = False)
    delFlag = models.BooleanField(default = False)

class dayWiseRitual(models.Model):
    eventId = models.CharField(max_length = 255) #from event table
    dayWiseRitualId = models.AutoField(primary_key = True)
    ritualName = models.CharField(max_length = 255)
    ritualNameO = models.CharField(max_length = 255)
    date = models.DateField()
    specialDay = models.BooleanField(default = False)
    createDate = models.DateTimeField(auto_now_add = True)
    modifyDate = models.DateTimeField(auto_now = False)
    delFlag = models.BooleanField(default = False)

class timeWiseRitual(models.Model):    
    timeWiseRitualId = models.AutoField(primary_key = True)
    eventId = models.CharField(max_length = 255) #from event table
    dayWiseRitualId = models.CharField(max_length = 255) #from day wise ritual table
    ritualName = models.CharField(max_length = 255)
    ritualNameO = models.CharField(max_length = 255)
    time = models.TimeField()
    createDate = models.DateTimeField(auto_now_add = True)
    modifyDate = models.DateTimeField(auto_now = False)
    delFlag = models.BooleanField(default = False)

class waterSpots(models.Model):    
    waterSpotsId = models.AutoField(primary_key = True)
    eventId = models.CharField(max_length = 255) #from event table
    name = models.CharField(max_length = 255, null=True, blank=True)
    nameO =models.CharField(max_length = 255, null=True, blank=True)   
    location = models.CharField(max_length = 255)
    locationO = models.CharField(max_length = 255)
    latitude = models.DecimalField(max_digits = 10, decimal_places = 8)
    longitude = models.DecimalField(max_digits = 10, decimal_places = 8)
    openingTime = models.TimeField()
    openingTimeO = models.TimeField()
    closingTime = models.TimeField()
    closingTimeO = models.TimeField()
    message = models.CharField(max_length = 255, null=True, blank=True)
    messageO = models.CharField(max_length = 255, null=True, blank=True)
    working = models.BooleanField()
    createDate = models.DateTimeField(auto_now_add = True)
    modifyDate = models.DateTimeField(auto_now = False)
    delFlag = models.BooleanField(default = False)

class hotels(models.Model):      
    hotelId = models.AutoField(primary_key = True)
    eventId = models.CharField(max_length = 255) #from event table
    name = models.CharField(max_length = 255, null=True, blank=True)
    nameO =models.CharField(max_length = 255, null=True, blank=True)   
    location = models.CharField(max_length = 255, null=True, blank=True)
    locationO = models.CharField(max_length = 255, null=True, blank=True)
    latitude = models.DecimalField(max_digits = 10, decimal_places = 8)
    longitude = models.DecimalField(max_digits = 10, decimal_places = 8)
    openingTime = models.TimeField()
    openingTimeO = models.TimeField()
    closingTime = models.TimeField()
    closingTimeO = models.TimeField()
    message = models.CharField(max_length = 255, null=True, blank=True)
    messageO = models.CharField(max_length = 255, null=True, blank=True)
    contactNumber = models.CharField(max_length = 13, null=True, blank=True)
    alternateNumber = models.CharField(max_length = 13, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    starRating = models.CharField(max_length = 13, null=True, blank=True)
    createDate = models.DateTimeField(auto_now_add = True)
    modifyDate = models.DateTimeField(auto_now = False)
    delFlag = models.BooleanField(default = False)