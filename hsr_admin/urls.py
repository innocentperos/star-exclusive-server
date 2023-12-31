from django.urls import path
from . import views

app_name = "hsr_admin"
urlpatterns = [
    path("", views.index, name="index"),
    path("logout/", views.user_logout, name="logout"),

    path("home/", views.home, name="home"),
    path("categories/", views.category_list, name="category_list"),
    path("categories/new/", views.new_category, name="new_category"),
    path("categories/<int:pk>/", views.view_category, name="view_category"),

    path("rooms/", views.room_list, name="room_list"),
    path("rooms/<int:pk>/", views.view_room, name="view_room"),

    path("reservations/", views.reservation_list, name="reservation_list"),
    path("reservations/new/", views.new_reservation, name="new_reservation"),
    path("reservations/check/", views.check_availability, name="check_availability"),
    path(
        "reservations/<int:pk>/delete/",
        views.delete_reservation,
        name="delete_reservation",
    ),
    path("reservations/<int:pk>/", views.view_reservation, name="view_reservation"),
]
