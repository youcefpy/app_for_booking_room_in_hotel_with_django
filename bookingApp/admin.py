from django.contrib import admin
from .models import Appartment,AppartImages, Booking,Contact
# Register your models here.



admin.site.register(Contact)
admin.site.register(Appartment)
admin.site.register(AppartImages)
admin.site.register(Booking)

