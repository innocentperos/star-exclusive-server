from rest_framework.viewsets import ViewSet
from rest_framework.request import Request
from rest_framework.response import Response

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from rest_framework import status

from .serializers import RoomCategorySerializer, RoomSerializer, SecureReservationSerializer

from .models import Reservation, Room, RoomCategory

class RoomCategoryViewSet(ViewSet):

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self,request):
        querysets = RoomCategory.objects.all()
        return Response(
            RoomCategorySerializer(querysets, many = True).data
        )
    
    def detail(self, request:Request, pk = None):
        """
        TO get a specific room category with the id as pk
        Returns
            200: If a category exists
            404: If no category with that id exist
            500: Something went wrong on the server
        """

        try:
            category = RoomCategory.objects.get(pk = pk)
            return Response(
                RoomCategorySerializer(category).data
            )
        except RoomCategory.DoesNotExist:

            return Response(
                status= status.HTTP_404_NOT_FOUND,
                data = {
                    "detail":"Room Category Not Found"
                }
            )
    
    @action(methods=("GET",), detail=True)
    def rooms(self, request:Request, pk = None):
        """
        Returns the list of the rooms that has been
        categorized under the current room categroy with the 
        id = pk 
        Returns
            200: List of the rooms 
            404: The category was not found
        """

        try:
            category = RoomCategory.objects.get(pk = pk)
            return Response(
                RoomSerializer(category.rooms, many = True).data
            )
        except RoomCategory.DoesNotExist:

            return Response(
                status= status.HTTP_404_NOT_FOUND,
                data = {
                    "detail":"Room Category Not Found"
                }
            )

class ReservationViewSet(ViewSet):

    def list(self, request:Request):

        reservations = Reservation.objects.all()
        return Response(
            SecureReservationSerializer(
            reservations,
            many = True
            ).data
        )
    
    
    