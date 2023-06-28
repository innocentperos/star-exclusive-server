from django import forms
from .models import Reservation


class NewCustomerForm(forms.ModelForm):
    class Meta:
        fields = (
            "first_name",
            "last_name",
            "id_type",
            "id_number",
            "email_address",
            "phone_number",
        )


class NewReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = (
            "arrival_date",
            "departure_date",
            "guest_count",
            "guests",
            "customization_request",
        )
