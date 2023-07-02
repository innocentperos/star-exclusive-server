from rest_framework.viewsets import ViewSet
from rest_framework.request import Request
from rest_framework.response import Response

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from rest_framework import status

from django.db.models import Q, F
from django.utils.dateparse import parse_datetime
from django.utils.datetime_safe import datetime

from .forms import NewCustomerForm, NewReservationForm


from .serializers import (
    ReservationSerializer,
    RoomCategorySerializer,
    RoomSerializer,
    SecureReservationSerializer,
)

from .models import Reservation, Room, RoomCategory
from .managers import RoomManager


class RoomCategoryViewSet(ViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request):
        querysets = RoomCategory.objects.all()
        return Response(RoomCategorySerializer(querysets, many=True).data)

    def detail(self, request: Request, pk=None):
        """
        TO get a specific room category with the id as pk
        Returns
            200: If a category exists
            404: If no category with that id exist
            500: Something went wrong on the server
        """

        try:
            category = RoomCategory.objects.get(pk=pk)
            return Response(RoomCategorySerializer(category).data)
        except RoomCategory.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"detail": "Room Category Not Found"},
            )

    @action(methods=("GET",), detail=True)
    def rooms(self, request: Request, pk=None):
        """
        Returns the list of the rooms that has been
        categorized under the current room categroy with the
        id = pk
        Returns
            200: List of the rooms
            404: The category was not found
        """

        try:
            category = RoomCategory.objects.get(pk=pk)
            return Response(RoomSerializer(category.rooms, many=True).data)
        except RoomCategory.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"detail": "Room Category Not Found"},
            )

    @action(methods=("GET",), detail=False)
    def available_rooms(self, request: Request):
        departure = request.query_params.get("departure")
        arrival = request.query_params.get("arrival")

        print(departure)
        print(arrival)

        if not departure:
            return Response(
                {"detail": "Departure date is required but was not provided"},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )
        if not arrival:
            return Response(
                {"detail": "Arrival date is required but was not provided"},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )

        arrival_date = parse_datetime(arrival)
        departure_date = parse_datetime(departure)

        if not arrival_date:
            return Response(
                {
                    "detail": "An invalid arrival date was provided, make sure it is a valid date"
                },
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )

        if not departure_date:
            return Response(
                {
                    "detail": "An invalid departure date was provided, make sure it is a valid date"
                },
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )

        current_date = datetime.now()
        current_arrival_date_delta = arrival_date - current_date
        departure_arrival_date_delta = departure_date - arrival_date

        if current_arrival_date_delta.total_seconds() < 60 * 59:
            #   The arrival date is not an hour ahead of the current date
            return Response(
                {
                    "detail": "Arrival date should atless be an hour ahead of the current date and time, consider increasing the arrival date or time"
                },
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )

        if departure_arrival_date_delta.total_seconds() < 60 * 60 * 11.9:
            #   The departure date is not 12 hour ahead of the arrival date
            return Response(
                {
                    "detail": "Departure date should atless be 12 hourw ahead of the your arrival date and time, consider increasing the departure date or time"
                },
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )

        available_rooms = RoomManager.available_rooms(None, arrival_date, departure_date)
        return Response(
            {
                "rooms":RoomSerializer(available_rooms, many = True).data,
                "categories":RoomCategorySerializer(RoomManager.extract_categories(available_rooms), many = True).data,
            }
        )


class ReservationViewSet(ViewSet):
    def list(self, request: Request):
        before = request.query_params.get("before", None)
        after = request.query_params.get("after", None)

        reservations = Reservation.objects.all()

        if before:
            try:
                before = parse_datetime(before)
                if before != None:
                    reservations.filter(departure_date__lte=before)
            except Exception as e:
                pass

        if request.user.is_anonymous:
            return Response(SecureReservationSerializer(reservations, many=True).data)

        else:
            return Response(ReservationSerializer(reservations, many=True).data)

    def retrieve(self, request: Request, pk=None):
        try:
            reservation = Reservation.objects.get(pk=pk)

            return Response(
                SecureReservationSerializer(
                    reservation,
                ).data
            )
        except Reservation.DoesNotExist:
            return Response(
                {"detail": "No reservation found that matches the provided pk"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @action(("POST",), detail=False)
    def make_reservation(self, request: Request):
        customer_form = NewCustomerForm(request.data)
        reservation_form = NewReservationForm(request.data)

        if not customer_form.is_valid():
            return Response(
                {
                    "detail": "Customer data field is missing",
                    "form": "customer",
                    "error": customer_form.errors,
                }
            )

        if not reservation_form.is_valid():
            return Response(
                {
                    "detail": "Customer data field is missing",
                    "form": "reservation",
                    "error": reservation_form.errors,
                }
            )

        return Response({"detail": "Dummy response"})

        pass
