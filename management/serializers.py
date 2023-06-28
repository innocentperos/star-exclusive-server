from rest_framework import serializers

from .models import Customer, Reservation, Room, RoomCategory


class RoomCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomCategory
        fields = ("pk", "title", "description", "cover")


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ("pk", "number", "category", "description", "unique", "addon")


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = (
            "first_name",
            "last_name",
            "id_type",
            "id_number",
            "email_address",
            "phone_number",
        )

class SecureCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = (
            "first_name",
            "last_name",
            "id_type",
            "secure_id_number",
            "secure_email_address",
            "secure_phone_number",
        )


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = (
            "room",
            "customer",
            "reservation_type",
            "arrival_date",
            "departure_date",
            "reservated_on",
            "stay",
            "guest_count",
            "guests",
            "customization_request",
            "paid",
            "payment",
            "canceled",
            "canceled_on",
        )


class SecureReservationSerializer(serializers.ModelSerializer):

    customer = SecureCustomerSerializer()
    class Meta:
        model = Reservation
        fields = (
            "room",
            "customer",
            "reservation_type",
            "arrival_date",
            "departure_date",
            "reservated_on",
            "stay",
            "guest_count",
            "guests",
            "customization_request",
            "paid",
            "payment",
            "canceled",
            "canceled_on",
        )

