from django import forms
from management.models import Reservation, RoomCategory


class LoginForm(forms.Form):
    email_address = forms.EmailField()
    password = forms.CharField()


class ReservationForm(forms.ModelForm):
    """Form definition for Reservaton."""

    class Meta:
        """Meta definition for Reservatonform."""

        model = Reservation
        fields = "__all__"


class CheckAvailabilityForm(forms.Form):
    arrival_date = forms.DateField()
    arrival_time = forms.TimeField()

    departure_date = forms.DateField()
    departure_time = forms.TimeField()


class CustomerForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email_address = forms.EmailField()
    phone_number = forms.CharField()
    identification_type = forms.CharField()
    identification_number = forms.CharField()
    


class BookingForm(forms.Form):
    room = forms.IntegerField()


class CategoryForm(forms.ModelForm):
    class Meta:
        model = RoomCategory
        fields = "__all__"

class RoomFilterForm(forms.Form):
    start_date = forms.DateField()
    start_time = forms.TimeField()
    end_date = forms.DateField()
    end_time = forms.TimeField()
    
class RoomUpdateForm(forms.Form):
    room_number = forms.CharField()
    description = forms.CharField()
    category = forms.ModelChoiceField(RoomCategory.objects.all())

class CategoryUpdateForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField()
    price = forms.FloatField()