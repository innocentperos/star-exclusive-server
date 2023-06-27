from rest_framework.routers import DefaultRouter

router = DefaultRouter()

from management.viewsets import RoomCategoryViewSet

router.register("categories",RoomCategoryViewSet, basename="RoomCategory")

# Add router viewsets