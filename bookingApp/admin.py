from django.contrib import admin
from .models import Room,RoomImages, Booking,Contact,CommentRoom,Category
# Register your models here.


class CategotyAdmin(admin.ModelAdmin):
    model = Category
    list_display=['id','name_category']


class RoomAdmin(admin.ModelAdmin):
    model = Room
    list_display = ['id','category_room','space','beds','bath','adult','child','description','price_per_night','is_available','created_at']


class BookingAdmin(admin.ModelAdmin):
    model = Booking
    list_display = ['id','user','room','name','phone_number','date_enter','date_out','total','is_paied','created_at']

admin.site.register(Category,CategotyAdmin)
admin.site.register(Room,RoomAdmin)
admin.site.register(Booking,BookingAdmin)
admin.site.register(Contact)
admin.site.register(RoomImages)
admin.site.register(CommentRoom)
