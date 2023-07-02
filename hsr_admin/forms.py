from django import forms
from management.models import Reservation

class LoginForm (forms.Form):

    email_address = forms.EmailField()
    password = forms.CharField()

class ReservationForm(forms.ModelForm):
    """Form definition for Reservaton."""

    class Meta:
        """Meta definition for Reservatonform."""

        model = Reservation
        fields = "__all__"
        
