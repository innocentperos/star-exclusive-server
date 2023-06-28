from rest_framework.routers import DefaultRouter

router = DefaultRouter()

from management.viewsets import (RoomCategoryViewSet,
ReservationViewSet)

router.register("categories",RoomCategoryViewSet, basename="RoomCategory")
router.register("reservations", ReservationViewSet, basename = "Reservation")
# Add router viewsets