"""rathyatraBackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from APIs import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    #image upload
    path("imageUpload/", views.imageUpload),
    path("getImage/", views.getImage),
    #Beat Box
    # path("getParkingTransaction/", views.getParkingTransaction),
    #Beat Box
    path("getBeatBox/", views.getBeatBox),
    #login
    path("login/", views.login),
    path("deleteData/<page>/<date>",views.deleteData),
    # path("generalUserLogin/", views.generalUserLogin),
    path("generalUserRegistration/", views.generalUserRegistration),
    #category
    path("getCategory/", views.getCtegory),
    #facilites
    path("getFaclities/", views.getFaclities),
    # path("event/",views.eve),
    # #parking
    path("prkng/",views.prkng),
    path("getParking/<page>/",views.getParking),
    path("getParkingList/",views.getParkingList),
    path("getParkingById/<id>/",views.getParkingById),
    path("updateParkingById/", views.updateParkingById),
    # path("postImage/", views.postImage),
    # # path("getParkingDetails/", views.getParkingDetails),
    # # path("getParkingDetailById/<id>/", views.getParkingDetailById),
    # # path("updateParkingById/", views.updateParkingById),
    # #SOS
    path("getGrievance/<page>/<date>", views.getGrievance),
    path("getGrievanceById/<id>/", views.getGrievanceById),
    path("postGrievance/",views.postGrievance),
    path("updateGrievanceById/", views.updateGrievanceById),
    path("filterGrievanceItem/<page>/", views.filterGrievanceItem),
    path("getGrivanceByNumber/<page>/", views.getGrivanceByNumber),
    # #lost
    path("postLostItem/", views.postLostItem),
    path("getLostItem/<page>/<date>", views.getLostItem),
    path("getLostItemById/<id>/", views.getLostItemById),
    path("updateLostItemById/", views.updateLostItemById),
    path("searchLostItem/", views.searchLostItem),
    path("filterLostItem/<page>/", views.filterLostItem),
    path("getLostItemByNumber/<page>/", views.getLostItemByNumber),
    # path("getLostItems/", views.getLostItems),
    # path("getLostItemsById/<id>/", views.getLostItemsById),
    # path("hideLostItemsById/", views.hideLostItemsById),
    # path("postLostItems/", views.postLostItems),
    # path("updateLostItemsById/", views.updateLostItemsById),
    # path("searchLostTokenPhoneNumber/<data>/", views.searchLostTokenPhoneNumber),
    # #found
    path("postFoundItem/", views.postFoundItem),
    path("getFoundItem/<page>/<date>",views.getFoundItem),    
    path("getFoundItemById/<id>/",views.getFoundItemById),
    path("hideFoundItemById/<id>/",views.hideFoundItemById),    
    path("updateFoundItemById/",views.updateFoundItemById),   
    path("filterFoundItem/<page>/",views.filterFoundItem),
    # path("getFoundItems/", views.getFoundItems),
    # path("getFoundItemById/<id>/", views.getFoundItemById),
    # path("hideFoundItemsById/", views.hideFoundItemsById),
    # path("postFoundItems/", views.postFoundItems),
    # path("updateFoundItemsById/", views.updateFoundItemsById),
    #medical Facility
    path("getMedicalFacility/<page>/",views.getMedicalFacility),    
    path("getMedicalFacilityById/<id>/",views.getMedicalFacilityById),
    #medical Facility
    path("getFoodDistribution/<page>/",views.getFoodDistribution),    
    path("getFoodDistributionById/<id>/",views.getFoodDistributionById),
    # path("foodDistributionByDate/<page>/",views.foodDistributionByDate),
    path("filterFoodDistribution/<page>/",views.filterFoodDistribution),
    #washroom
    path("getWashroom/<page>/",views.getWashroom),  
    #shoe stand
    path("getShoeStand/<page>/",views.getShoeStand), 
    #rituals
    path("getDayWiseRituals/",views.getDayWiseRituals), 
    path("getRitualsById/<id>/",views.getRitualsById),   
    #Water Spots
    path("getWaterSpots/<page>/",views.getWaterSpots), 
    #Hotels
    path("getHotels/<page>/",views.getHotels),
    path("filterHotel/<page>/",views.filterHotel),
    path("postHotel/",views.postHotel),
    path("deleteHotel/",views.deleteHotel), 


]  
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)