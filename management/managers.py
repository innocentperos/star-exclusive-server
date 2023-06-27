from .models import Room, RoomCategory, Reservation
from django.utils.datetime_safe import datetime
from django.db.models import Q, QuerySet


class RoomManager:
    def available_rooms(
        category: RoomCategory, start_date: datetime, end_date: datetime
    ):
        reservations = Reservation.objects.filter(
            Q(arrival_date=start_date)
            | Q(departure_date=start_date)
            | Q(departure_date=start_date)
            | Q(departure_date=end_date)
            | Q(arrival_date__gte=start_date) & Q(departure_date__lte=end_date)
            | Q(arrival_date__lte=start_date) & Q(departure_date__gte=start_date)
            | Q(arrival_date_lte=end_date) & Q(departure_date_gte=end_date)
            | Q(arrival_date__lte=start_date) & Q(departure_date_gte=end_date)
        )
        # Get reservations that falls within the start and end date

        # Get all the rooms under that category and remove each room of each reservation
        rooms: QuerySet = category.rooms

        for reservation in reservations:
            rooms = rooms.exclude(pk=reservation.room)
        # return the remaining rooms
        return rooms
