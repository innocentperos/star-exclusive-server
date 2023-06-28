from django.contrib import admin
from .models import Reservation, Room, Payment, AddOn, RoomCategory, Customer

# Register your models here.


@admin.register(RoomCategory)
class RoomCategoryAdminModel(admin.ModelAdmin):
    list_display = ("pk", "title", "price", "description")


@admin.register(Room)
class RoomAdminModel(admin.ModelAdmin):

    list_display = ("pk", "title", "category")

    @admin.display
    def title(self, model, *args, **kwargs):
        return str(model)
    

@admin.register(AddOn)
class AddOnAdminModel(admin.ModelAdmin):
    list_display = ("pk","title","price","category", "description",)

    search_fields = ("title",)

@admin.register(Customer)
class CustomerAdminModel(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "id_type",
        "id_number",
        "email_address",
        "phone_number",
    )

    search_fields = ("email_address","id_number","phone_number","first_name","last_name")
  
@admin.register(Reservation)
class ReservationAdminModel(admin.ModelAdmin):
  list_display = (
      "room",
      "customer",
      "reservation_type",
      "arrival_date",
      "departure_date",
      "paid",
      "payment",
      "reservated_on",
      "guest_count",
      "cancelled"
    )
    
  search_fields = ("customer__first_name","room__number")
