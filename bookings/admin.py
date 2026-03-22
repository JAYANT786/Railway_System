from django.contrib import admin
from .models import Booking

class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'train', 'seats_booked', 'journey_date', 'created_at')

admin.site.register(Booking, BookingAdmin)