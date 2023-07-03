from .models import Room, RoomCategory, Reservation
from django.utils.datetime_safe import datetime
from django.db.models import Q, QuerySet


class RoomManager:
    @staticmethod
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
            | Q(arrival_date__lte=end_date) & Q(departure_date__gte=end_date)
            | Q(arrival_date__lte=start_date) & Q(departure_date__gte=end_date)
        )
        # Get reservations that falls within the start and end date

        # Get all the rooms under that category and remove each room of each reservation
        # rooms: QuerySet = category.rooms

        rooms = Room.objects.all()
        if category:
            rooms = Room.objects.filter(category=category)

        for reservation in reservations:
            rooms = rooms.exclude(pk=reservation.room.pk)

        # return the remaining rooms
        return rooms

    @staticmethod
    def extract_categories(rooms: list[Room]) -> list[RoomCategory]:
        categories = []
        categories_id = set()

        for room in rooms:
            if room.category.pk not in categories_id:
                categories.append(room.category)
                categories_id.add(room.category.pk)

        return categories
