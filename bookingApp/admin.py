from django.contrib import admin
from .models import Appartment, Booking,Contact
# Register your models here.



admin.site.register(Contact)
admin.site.register(Appartment)
admin.site.register(Booking)