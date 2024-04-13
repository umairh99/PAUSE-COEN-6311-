from django.contrib import admin
from .models import Agency, Package, Flight, Hotel, Activity, Photo, CustomPackage, Booking, Payment

admin.site.register(Agency)
admin.site.register(Photo)
admin.site.register(Package)
admin.site.register(Flight)
admin.site.register(Hotel)
admin.site.register(Activity)
admin.site.register(CustomPackage)
admin.site.register(Booking)
admin.site.register(Payment)
