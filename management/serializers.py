from rest_framework import serializers

from .models import Customer, Room, RoomCategory

class RoomCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = RoomCategory
        fields = ("pk","title","description", "cover")

class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ("pk","number","category","description","unique","addon")

class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'id_type', 'id_number', 'email_address', 'phone_number', )