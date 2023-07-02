from django.urls import path
from . import views

app_name = "hsr_admin"
urlpatterns = [
    path("", views.index, name="index"),
    path("home/", views.home, name="home"),
    path("categories/", views.category_list, name="category_list"),
    path('reservations/', views.reservation_list, name='reservation_list'),
    path('reservations/new/', views.new_reservation, name='new_reservation'),
    path('reservations/<int:pk>/delete/', views.delete_reservation, name='delete_reservation'),
    path('reservations/<int:pk>/', views.view_reservation, name='view_reservation'),
]