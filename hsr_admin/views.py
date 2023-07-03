from django.shortcuts import get_object_or_404, render, redirect
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db.models import Q, F
from django.db import transaction
from django.utils.dateparse import parse_datetime


from management.models import RoomCategory, Room, Customer, Reservation
from management.managers import RoomManager

from .forms import (
    BookingForm,
    CheckAvailabilityForm,
    CustomerForm,
    LoginForm,
    ReservationForm,
)

# Create your views here.


def index(request: HttpRequest):
    if request.method.upper() == "POST":
        form = LoginForm(request.POST)

        if not form.is_valid():
            return render(
                request,
                template_name="hsr_admin/index.html",
                context={
                    "message": "Please provide a valid email address and password"
                },
            )

        try:
            data = form.cleaned_data
            user = User.objects.get(
                Q(email=data["email_address"]) | Q(username=data["email_address"])
            )
            if user.check_password(data["password"]):
                login(request, user)
                return redirect(home)
        except User.DoesNotExist:
            pass

        return render(
            request,
            template_name="hsr_admin/index.html",
            context={"message": "Wrong email address or password"},
        )

    return render(request, template_name="hsr_admin/index.html")


def home(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect(index)
    return render(request, template_name="hsr_admin/dashboard.html", context={})


def category_list(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect(index)

    _categories = RoomCategory.objects.all()
    return render(
        request,
        template_name="hsr_admin/categories.html",
        context={"categories": _categories},
    )


def reservation_list(request: HttpRequest):
    reservations = Reservation.objects.all()
    return render(
        request, "hsr_admin/reservation_list.html", {"reservations": reservations}
    )


def delete_reservation(request, pk):
    reservation = Reservation.objects.get(pk=pk)

    if request.method == "POST":
        reservation.delete()
        return redirect("hsr_admin:reservation_list")

    return render(
        request, "hsr_admin/delete_reservation.html", {"reservation": reservation}
    )


def view_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)

    return render(
        request, "hsr_admin/view_reservation.html", {"reservation": reservation}
    )


def check_availability(request: HttpRequest):
    form = CheckAvailabilityForm(request.POST)

    if not form.is_valid():
        return render(
            request,
            "hsr_admin/new_reservation.html",
            context={
                "message": "Please provide the reservation arrival and departure date and date",
                "form": request.POST,
            },
        )
    data = form.cleaned_data

    arrival = parse_datetime(f"{data['arrival_date']} {data['arrival_time']}")
    departure = parse_datetime(f"{data['departure_date']} {data['departure_time']}")

    if not arrival or not departure:
        return render(
            request,
            "hsr_admin/new_reservation.html",
            context={
                "message": "Please provide the reservation arrival and departure date and date",
                "form": request.POST,
            },
        )

    if departure <= arrival:
        return render(
            request,
            "hsr_admin/new_reservation.html",
            context={
                "message": "Please departure date most be be ahead of arrival date",
                "form": request.POST,
            },
        )

    rooms = RoomManager.available_rooms(None, arrival, departure)
    categories = RoomManager.extract_categories(rooms)

    colors = [
        "bg-red-700",
        "bg-indigo-700",
        "bg-green-700",
        "bg-purple-700",
        "bg-pink-700",
        "bg-violet-700",
    ]
    _colors = {}

    for cat in categories:
        _colors[cat.pk] = colors[cat.pk % len(categories)]

    return render(
        request,
        "hsr_admin/new_reservation.html",
        context={
            "adding": True,
            "form": request.POST,
            "categories": categories,
            "rooms": rooms,
            "colors": _colors,
        },
    )


def new_reservation(request: HttpRequest):
    if request.method == "POST":

        form = CheckAvailabilityForm(request.POST)
        customer_form = CustomerForm(request.POST)
        booking_form = BookingForm(request.POST)

        if not form.is_valid():
            return render(
                request,
                "hsr_admin/new_reservation.html",
                context={
                    "message": "1 Please provide the reservation arrival and departure date and date",
                    "form": request.POST,
                },
            )
        
        #Check the reservation Form
        data = form.cleaned_data

        arrival = parse_datetime(f"{data['arrival_date']} {data['arrival_time']}")
        departure = parse_datetime(f"{data['departure_date']} {data['departure_time']}")

        if not arrival or not departure:
            return render(
                request,
                "hsr_admin/new_reservation.html",
                context={
                    "message": "2 Please provide the reservation arrival and departure date and date",
                    "form": request.POST,
                },
            )

        if departure <= arrival:
            return render(
                request,
                "hsr_admin/new_reservation.html",
                context={
                    "message": "3 Please departure date most be be ahead of arrival date",
                    "form": request.POST,
                },
            )
        
        if not customer_form.is_valid():
            rooms = RoomManager.available_rooms(None, arrival, departure)
            categories = RoomManager.extract_categories(rooms)

            colors = [
                "bg-red-700",
                "bg-indigo-700",
                "bg-green-700",
                "bg-purple-700",
                "bg-pink-700",
                "bg-violet-700",
            ]
            _colors = {}

            for cat in categories:
                _colors[cat.pk] = colors[cat.pk % len(categories)]

            return render(
                request,
                "hsr_admin/new_reservation.html",
                context={
                    "adding": True,
                    "form": request.POST,
                    "categories": categories,
                    "rooms": rooms,
                    "colors": _colors,
                },
            )
        
        if not booking_form.is_valid():
            rooms = RoomManager.available_rooms(None, arrival, departure)
            categories = RoomManager.extract_categories(rooms)

            colors = [
                "bg-red-700",
                "bg-indigo-700",
                "bg-green-700",
                "bg-purple-700",
                "bg-pink-700",
                "bg-violet-700",
            ]
            _colors = {}

            for cat in categories:
                _colors[cat.pk] = colors[cat.pk % len(categories)]

            return render(
                request,
                "hsr_admin/new_reservation.html",
                context={
                    "adding": True,
                    "form": request.POST,
                    "categories": categories,
                    "rooms": rooms,
                    "colors": _colors,
                },
            )
        
        customer_data = customer_form.cleaned_data
        customer = Customer(
            first_name = customer_data["first_name"],
            last_name = customer_data["last_name"],
            email_address = customer_data["email_address"],
            phone_number = customer_data["phone_number"],
            id_type = customer_data["identification_type"],
            id_number = customer_data["identification_number"],
        )

        reservation_data = form.cleaned_data
        booking_data = booking_form.cleaned_data

        reservation = Reservation(
            customer = customer,
            reservation_type = Reservation.RESERVATION,
            arrival_date = arrival,
            departure_date = departure,
            paid = True,
            room = booking_data["room"]
        )

        with transaction.atomic():

            customer.save()
            reservation.save()

            return redirect(reservation_list)

    else:
        form = ReservationForm()

    return render(request, "hsr_admin/new_reservation.html", {"form": form})
