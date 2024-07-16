
import datetime
from bookingApp.models import Appartment,Booking

def booking_logic(apprt,check_in,check_out):
    availability_list = []

    booking_list = Booking.objects.filter(appart=apprt)

    for booking in booking_list:
        if booking.date_enter>check_out or booking.date_out < check_in:
            availability_list.append(True)
        else :
            availability_list.append(False)

    return all(availability_list)
