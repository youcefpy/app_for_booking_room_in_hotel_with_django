
import datetime
from bookingApp.models import Room,Booking

def booking_logic(room,check_in,check_out):
    availability_list = []

    booking_list = Booking.objects.filter(room=room)

    for booking in booking_list:
        if booking.date_enter>check_out or booking.date_out < check_in:
            availability_list.append(True)
        else :
            availability_list.append(False)

    return all(availability_list)
