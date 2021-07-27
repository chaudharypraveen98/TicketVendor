from django.contrib import admin

# Register your models here.
from booking.models import Seat, Orders

admin.site.register(Seat)
admin.site.register(Orders)
