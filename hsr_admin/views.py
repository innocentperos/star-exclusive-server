from django.shortcuts import get_object_or_404, render, redirect
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.db.models import Q, F
from django.db import transaction
from django.utils.dateparse import parse_datetime
from django.utils.datetime_safe import datetime

from management.models import RoomCategory, Room, Customer, Reservation
from management.managers import RoomManager

from .forms import (
    BookingForm,
    CategoryUpdateForm,
    CheckAvailabilityForm,
    CustomerForm,
    LoginForm,
    ReservationForm,
    CategoryForm,
    RoomFilterForm,
    RoomUpdateForm,
)

# Create your views here.


def new_reservations():
    return Reservation.objects.filter(viewed=False).count()


def context_parse(context):
    context["status__"] = new_reservations()
    context["status__category"] = RoomCategory.objects.all().count()
    context["status__room"] = Room.objects.all().count()

    return context


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
                return redirect("hsr_admin:home")
        except User.DoesNotExist:
            pass

        return render(
            request,
            template_name="hsr_admin/index.html",
            context={"message": "Wrong email address or password"},
        )

    if request.user.is_authenticated:
        return redirect("hsr_admin:home")

    return render(request, template_name="hsr_admin/index.html")


def user_logout(request: HttpRequest):
    if request.user.is_authenticated:
        logout(request)

    return redirect("hsr_admin:index")


def home(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect(index)
    return render(
        request, template_name="hsr_admin/dashboard.html", context=context_parse({})
    )


def category_list(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect(index)

    _categories = RoomCategory.objects.all()
    return render(
        request,
        template_name="hsr_admin/categories.html",
        context=context_parse({"categories": _categories}),
    )


def new_category(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect(index)

    if request.method == "GET":
        return render(request, "hsr_admin/new_category.html", context=context_parse({}))

    form = CategoryForm(request.POST, request.FILES)

    if not form.is_valid():
        return render(
            request,
            "hsr_admin/new_category.html",
            context=context_parse(
                {"message": "Please provide all the fields", "form": request.POST}
            ),
        )
    category = form.save()

    rooms = request.POST.get("rooms")

    if rooms:
        try:
            rooms = int(rooms)
            for i in range(rooms):
                room = Room(category=category)
                room.save()
        except Exception as e:
            pass

    return redirect("hsr_admin:category_list")


def reservation_list(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect(index)

    reservations = Reservation.objects.filter(viewed=True).order_by("-id")
    new_reservations = Reservation.objects.filter(viewed=False).order_by("-id")

    return render(
        request,
        "hsr_admin/reservation_list.html",
        context_parse(
            {"reservations": reservations, "new_reservations": new_reservations}
        ),
    )


def room_list(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect(index)

    form = RoomFilterForm(request.GET)

    if form.is_valid():
        data = form.cleaned_data
        start_date = parse_datetime(f"{data['start_date']} {data['start_time']}")
        end_date = parse_datetime(f"{data['end_date']} {data['end_time']}")

        rooms = RoomManager.taken_rooms(start_date=start_date, end_date=end_date)
    else:
        rooms = Room.objects.all()

    categories = RoomCategory.objects.all()

    colors = [
        "bg-red-700",
        "bg-indigo-700",
        "bg-green-700",
        "bg-purple-700",
        "bg-pink-700",
        "bg-violet-900",
        "bg-brown-700",
        "bg-slate-900",
    ]
    _colors = {}

    for cat in categories:
        _colors[cat.pk] = colors[cat.pk % len(categories)]

    return render(
        request,
        "hsr_admin/rooms.html",
        context_parse(
            {
                "categories": categories,
                "rooms": rooms,
                "colors": _colors,
                "form": request.GET,
            }
        ),
    )


def view_room(request: HttpRequest, pk):
    if not request.user.is_authenticated:
        return redirect(index)

    try:
        room = Room.objects.get(pk=pk)
        categories = RoomCategory.objects.all()

        if request.method == "POST":
            form = RoomUpdateForm(request.POST)
            if not form.is_valid():
                return render(
                    request,
                    "hsr_admin/view_room.html",
                    context_parse(
                        {
                            "room": room,
                            "reservations": room.reservations.all(),
                            "categories": categories,
                            "error": "Please provide all field",
                        }
                    ),
                )

            data = form.data

            room.category = categories.get(pk=int(data.get("category")))
            room.number = data.get("room_number")
            room.description = data.get("description")

            room.save()

            return render(
                request,
                "hsr_admin/view_room.html",
                context_parse(
                    {
                        "room": room,
                        "reservations": room.reservations.all(),
                        "categories": categories,
                        "success": "Room detail Updated",
                    }
                ),
            )

        return render(
            request,
            "hsr_admin/view_room.html",
            context_parse(
                {
                    "room": room,
                    "reservations": room.reservations.all(),
                    "categories": categories,
                }
            ),
        )
    except Room.DoesNotExist:
        return redirect("hsr_admin:room_list")


def view_category(request: HttpRequest, pk):
    if not request.user.is_authenticated:
        return redirect(index)

    try:
        category = RoomCategory.objects.get(pk=pk)

        if request.method == "POST":
            form = CategoryUpdateForm(request.POST)
            if not form.is_valid():
                return render(
                    request,
                    "hsr_admin/view_category.html",
                    context_parse(
                        {
                            "rooms": category.rooms.all(),
                            "category": category,
                            "error": "Please provide all field",
                        }
                    ),
                )

            data = form.cleaned_data

            category.title = data.get("title")
            category.description = data.get("description")
            category.price = data.get("price")
            category.save()

            return render(
                request,
                "hsr_admin/view_category.html",
                context_parse(
                    {
                        "rooms": category.rooms.all(),
                        "category": category,
                        "success": "CAtegory detail Updated",
                    }
                ),
            )
        elif request.method == "PUT":
            print(request.body)

        return render(
            request,
            "hsr_admin/view_category.html",
            context_parse(
                {
                    "rooms": category.rooms.all(),
                    "category": category,
                }
            ),
        )
    except Room.DoesNotExist:
        return redirect("hsr_admin:category_list")


def delete_reservation(request, pk):
    if not request.user.is_authenticated:
        return redirect(index)

    reservation = Reservation.objects.get(pk=pk)

    reservation.viewed = True
    reservation.save()

    if request.method == "POST":
        reservation.delete()
        return redirect("hsr_admin:reservation_list")

    return render(
        request,
        "hsr_admin/delete_reservation.html",
        context_parse({"reservation": reservation}),
    )


def view_reservation(request, pk):
    if not request.user.is_authenticated:
        return redirect(index)

    try:
        reservation = Reservation.objects.get(pk=pk)

        reservation.viewed = True
        reservation.save()

        return render(
            request,
            "hsr_admin/view_reservation.html",
            context_parse({"reservation": reservation}),
        )

    except Reservation.DoesNotExist:
        return redirect("hsr_admin:reservation_list")


def check_availability(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect(index)

    form = CheckAvailabilityForm(request.POST)

    if not form.is_valid():
        return render(
            request,
            "hsr_admin/new_reservation.html",
            context=context_parse(
                {
                    "message": "Please provide the reservation arrival and departure date and date",
                    "form": request.POST,
                }
            ),
        )
    data = form.cleaned_data

    arrival = parse_datetime(f"{data['arrival_date']} {data['arrival_time']}")
    departure = parse_datetime(f"{data['departure_date']} {data['departure_time']}")

    if not arrival or not departure:
        return render(
            request,
            "hsr_admin/new_reservation.html",
            context=context_parse(
                {
                    "message": "Please provide the reservation arrival and departure date and date",
                    "form": request.POST,
                }
            ),
        )

    if departure <= arrival:
        return render(
            request,
            "hsr_admin/new_reservation.html",
            context=context_parse(
                {
                    "message": "Please departure date most be be ahead of arrival date",
                    "form": request.POST,
                }
            ),
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
        _colors[cat.pk] = colors[cat.pk % len(categories) + 1]

    return render(
        request,
        "hsr_admin/new_reservation.html",
        context=context_parse(
            {
                "adding": True,
                "form": request.POST,
                "categories": categories,
                "rooms": rooms,
                "colors": _colors,
            }
        ),
    )


def new_reservation(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect(index)

    if request.method == "POST":
        form = CheckAvailabilityForm(request.POST)
        customer_form = CustomerForm(request.POST)
        booking_form = BookingForm(request.POST)

        if not form.is_valid():
            return render(
                request,
                "hsr_admin/new_reservation.html",
                context=context_parse(
                    {
                        "message": "1 Please provide the reservation arrival and departure date and date",
                        "form": request.POST,
                    }
                ),
            )

        # Check the reservation Form
        data = form.cleaned_data

        arrival = parse_datetime(f"{data['arrival_date']} {data['arrival_time']}")
        departure = parse_datetime(f"{data['departure_date']} {data['departure_time']}")

        if not arrival or not departure:
            return render(
                request,
                "hsr_admin/new_reservation.html",
                context=context_parse(
                    {
                        "message": "2 Please provide the reservation arrival and departure date and date",
                        "form": request.POST,
                    }
                ),
            )

        if departure <= arrival:
            return render(
                request,
                "hsr_admin/new_reservation.html",
                context=context_parse(
                    {
                        "message": "3 Please departure date most be be ahead of arrival date",
                        "form": request.POST,
                    }
                ),
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
                context=context_parse(
                    {
                        "adding": True,
                        "form": request.POST,
                        "categories": categories,
                        "rooms": rooms,
                        "colors": _colors,
                    }
                ),
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
                context=context_parse(
                    {
                        "adding": True,
                        "form": request.POST,
                        "categories": categories,
                        "rooms": rooms,
                        "colors": _colors,
                    }
                ),
            )

        customer_data = customer_form.cleaned_data
        customer = Customer(
            first_name=customer_data["first_name"],
            last_name=customer_data["last_name"],
            email_address=customer_data["email_address"],
            phone_number=customer_data["phone_number"],
            id_type=customer_data["identification_type"],
            id_number=customer_data["identification_number"],
        )

        reservation_data = form.cleaned_data
        booking_data = booking_form.cleaned_data

        try:
            room = Room.objects.get(pk=booking_data["room"])
        except Room.DoesNotExist:
            return render(
                request,
                "hsr_admin/new_reservation.html",
                context=context_parse(
                    {
                        "adding": True,
                        "form": request.POST,
                        "categories": categories,
                        "rooms": rooms,
                        "colors": _colors,
                    }
                ),
            )

        reservation = Reservation(
            customer=customer,
            reservation_type=Reservation.RESERVATION,
            arrival_date=arrival,
            departure_date=departure,
            reservated_on=datetime.now(),
            paid=True,
            room=room,
        )

        with transaction.atomic():
            customer.save()
            reservation.save()

            return redirect("hsr_admin:reservation_list")

    else:
        form = ReservationForm()

    return render(
        request, "hsr_admin/new_reservation.html", context_parse({"form": form})
    )
