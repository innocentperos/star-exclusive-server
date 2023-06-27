from django.db import models
from django.utils.datetime_safe import datetime


class RoomCategory(models.Model):
    price = models.FloatField()
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    cover = models.ImageField(blank=True,upload_to="rooms")

    def __str__(self) -> str:
        return self.title

class AddOn(models.Model):
    """
    This identifies add-ons a guest can add into their reservation
    Example , like """
    category = models.ForeignKey(RoomCategory, on_delete=models.CASCADE, related_name="addons")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default="")
    price = models.FloatField()
    render = models.TextField(blank=True, null=True)
    cover = models.ImageField(blank=True,upload_to="rooms")


    def __str__(self):
        return f"{self.title} {self.price}"

class Room(models.Model):
    number = models.CharField(max_length=14, blank=True)
    category = models.ForeignKey(
        RoomCategory, related_name="rooms", on_delete=models.CASCADE
    )
    description = models.TextField(blank=True, null=True)
    unique = models.BooleanField(default=False)
    addon = models.JSONField(blank=True, default=dict)

    def __str__(self):
        return f"Room {self.pk}"


class Customer(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    id_type = models.CharField(max_length=255)
    id_number = models.CharField(max_length=25)
    email_address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=12)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Payment(models.Model):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"

    amount = models.FloatField()
    date = models.DateTimeField(default=datetime.now)
    status = models.CharField(
        max_length=25,
        choices=((PENDING, PENDING), (SUCCESS, SUCCESS), (FAILED, FAILED)),
        default=PENDING,
    )
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, related_name="payments"
    )

    description = models.JSONField(default=dict, null=True, blank=True)

    transaction_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    transaction_reference = models.CharField(max_length=50, unique=True, blank=True, null=True)

    def __str__(self):
        return f"{self.amount} ({self.status.title()})"

class Reservation(models.Model):
    RESERVATION = "reseravtion"
    BOOKING = "booking"
    room = models.ForeignKey(
        Room, related_name="reservations", on_delete=models.CASCADE
    )

    reservation_type = models.CharField(
        max_length=25, choices=((RESERVATION, RESERVATION), (BOOKING, BOOKING))
    )
    # The date the guest will arrive to the hotel
    arrival_date = models.DateTimeField()
    # The date the guest will be leaving the hotel
    departure_date = models.DateTimeField()
    #The date the guest made the reservation
    reservated_on = models.DateTimeField(auto_created=True)
    # The number of days the guest will be staying at the hotel
    stay = models.IntegerField(default=1)
    # The number of individuals the guest will be coming with
    guest_count = models.IntegerField(
        default=1,
    )
    # The information about the guest guest(s)
    guests = models.JSONField(default=list, blank=True)
    # The customization that the guest is requesting
    customization_request = models.JSONField(default=dict, blank=True, null=True)

    # If the guest has made a payment or not
    paid = models.BooleanField(default=False)
    payment = models.OneToOneField(Payment, null=True , on_delete= models.SET_NULL, related_name="reservation")

    # If the guest has canceled the request
    canceled = models.BooleanField(default=False)
    # The date the guest canceled the request
    canceled_on = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{'Paid' if self.paid else ''} {self.arrival_date.date} - {self.departure_date.date} | {self.room}"


# Create your models here.
