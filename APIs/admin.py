from django.contrib import admin
from . import models
# # Register your models here.
# # admin.site.register(models.Parking)
# # admin.site.register(models.Beat_box)
# # admin.site.register(models.Category)
# # admin.site.register(models.Lost_and_found)
# # admin.site.register(models.Role)
# # admin.site.register(models.User)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("categoryName", "categoryNameO",)

class EventAdmin(admin.ModelAdmin):
    list_display = ("eventName",)

class ParkingAdmin(admin.ModelAdmin):
    list_display = ("parkingName", "parkingId", "userId",)

class UserAdmin(admin.ModelAdmin):
    list_display = ("firstName", "contactNumber",)

class BeatBoxAdmin(admin.ModelAdmin):
    list_display = ("beatBoxDescription",)

class RoleAdmin(admin.ModelAdmin):
    list_display = ("roleId", "roleName", )

class dayWiseRitualAdmin(admin.ModelAdmin):
    list_display = ("ritualName",)

class facilitiesAdmin(admin.ModelAdmin):
    list_display = ("facilityType", "facilityName",)

class timeWiseRitualAdmin(admin.ModelAdmin):
    list_display = ("ritualName",)

class foodDistributionAdmin(admin.ModelAdmin):
    list_display = ("eventId", "name", )

class hotelAdmin(admin.ModelAdmin):
    list_display = ("eventId", "name", "starRating", )

class parking_user_XAdmin(admin.ModelAdmin):
    list_display = ("parkingId", "userId", )

admin.site.register(models.imageStorage)
admin.site.register(models.event, EventAdmin)
admin.site.register(models.beatBox, BeatBoxAdmin)
admin.site.register(models.category, CategoryAdmin)
admin.site.register(models.role, RoleAdmin)
admin.site.register(models.facilities, facilitiesAdmin)
admin.site.register(models.foodDistribution, foodDistributionAdmin)
admin.site.register(models.lostItem)
admin.site.register(models.foundItem)
admin.site.register(models.medicalFacility)
admin.site.register(models.parking, ParkingAdmin)
admin.site.register(models.parkingTransaction)
admin.site.register(models.shoeStand)
admin.site.register(models.grievance)
admin.site.register(models.vehicleType)
admin.site.register(models.washroom)
admin.site.register(models.user, UserAdmin)
admin.site.register(models.timeWiseRitual, timeWiseRitualAdmin)
admin.site.register(models.dayWiseRitual, dayWiseRitualAdmin)
admin.site.register(models.hotels, hotelAdmin)
admin.site.register(models.waterSpots)
admin.site.register(models.parking_user_X, parking_user_XAdmin)