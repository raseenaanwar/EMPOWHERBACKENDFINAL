from django.contrib import admin
from .models import Availability,Booking_session
# Register your models here.

# admin.site.register(Availability)
admin.site.register(Booking_session)
@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('mentor', 'date', 'start_time', 'end_time', 'duration')
    search_fields = ('mentor__user__email', 'date')

