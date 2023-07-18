from django.db import models
from django.forms import ValidationError
from django.utils.datetime_safe import datetime
import string
import random


class RoomCategory(models.Model):
    price = models.FloatField()
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    cover = models.FileField(blank=True, upload_to="rooms")

    def __str__(self) -> str:
        return self.title


class AddOn(models.Model):
    """
    This identifies add-ons a guest can add into their reservation
    Example , like"""

    category = models.ForeignKey(
        RoomCategory, on_delete=models.CASCADE, related_name="addons"
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default="")
    price = models.FloatField()
    render = models.TextField(blank=True, null=True)
    cover = models.FileField(blank=True, upload_to="rooms")

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
        if self.number:
            return f"Room {self.number}"
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

    @property
    def secure_id_number(self):
        value = self.id_number
        size = len(value)

        return f"{value[:2]}{'*'*(size-5)}{value[(size-3):size]}"

    @property
    def secure_email_address(self):
        value = self.email_address
        domain = value.split("@")
        address = domain[0]
        if len(domain) < 2:
            domain = ""
        else:
            domain = f"@{domain[1]}"

        size = len(address)

        return f"{address[:4]}{'*'*(size-4)}{domain}"

    @property
    def secure_phone_number(self):
        value = self.phone_number
        size = len(value)

        return f"{value[:4]}{'*'*(size-6)}{value[size-2:size]}"


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
    transaction_reference = models.CharField(
        max_length=50, unique=True, blank=True, null=True
    )

    def __str__(self):
        return f"{self.amount} ({self.status.title()})"


def validate_departure_date_greater_than_arrival_date(value):
    if value <= models.F("arrival_date"):
        raise ValidationError(
            _("Departure date must be greater than the arrival date.")
        )


def generate_reservation_code():

    prefix = "".join(random.choices(string.digits,k=4))
    suffix = "".join(random.choices(string.ascii_uppercase, k=3))

    return f"{suffix}{prefix}"

def generate_cancel_code():

    prefix = "".join(random.choices(string.digits,k=6))
    suffix = "".join(random.choices(string.ascii_uppercase, k=12))
    key = "".join(random.choices(string.ascii_letters + string.digits,k=8))

    return f"{suffix}{prefix}{key}"


class Reservation(models.Model):
    RESERVATION = "reseravtion"
    BOOKING = "booking"

    viewed = models.BooleanField(default=False)
    cancel_code = models.CharField(max_length=200, blank=True)

    room = models.ForeignKey(
        Room, related_name="reservations", on_delete=models.CASCADE
    )

    requirement = models.TextField(default="", blank=True)

    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, related_name="reservations"
    )

    code = models.CharField(unique=False, default = generate_reservation_code, max_length=50, blank=True,null = True)

    # Holds the customer information just incase the customer was deleted
    customer_raw = models.JSONField(null=True, blank=True, default=dict)

    reservation_type = models.CharField(
        max_length=25, choices=((RESERVATION, RESERVATION), (BOOKING, BOOKING))
    )
    # The date the guest will arrive to the hotel
    arrival_date = models.DateTimeField()
    # The date the guest will be leaving the hotel
    departure_date = models.DateTimeField()
    # departure_date = models.DateTimeField(validators=[validate_departure_date_greater_than_arrival_date])

    # The date the guest made the reservation
    reservated_on = models.DateTimeField(auto_created=True, blank=True)
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
    payment = models.OneToOneField(
        Payment,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="reservation",
    )

    # If the guest has canceled the request
    cancelled = models.BooleanField(default=False)
    # The date the guest canceled the request
    cancelled_on = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{'Paid' if self.paid else ''} {self.arrival_date.date()} - {self.departure_date.date()} | {self.room}"


# Create your models here.
