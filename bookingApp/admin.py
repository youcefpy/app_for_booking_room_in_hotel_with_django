from django.contrib import admin
from .models import Room,RoomImages, Booking,Contact,CommentRoom,Category
# Register your models here.



class RoomAdmin(admin.ModelAdmin):
    model = Room
    list_display = ['id','category_room','space','beds','bath','description','price_per_night','is_available']

admin.site.register(Category)
admin.site.register(Contact)
admin.site.register(Room,RoomAdmin)
admin.site.register(RoomImages)
admin.site.register(Booking)
admin.site.register(CommentRoom)
