from rest_framework import serializers
from . import models

class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.user
        fields = "__all__"

class grievanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.grievance
        fields = "__all__"

class foundItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.foundItem
        fields = "__all__"

class parkingTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.parkingTransaction
        fields = "__all__"


class lostItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.lostItem
        fields = "__all__"

class imageStorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.imageStorage
        fields = "__all__"

class hotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.hotels
        fields = "__all__"