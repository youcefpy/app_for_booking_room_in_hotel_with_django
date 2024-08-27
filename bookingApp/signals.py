from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received
from django.dispatch import receiver

from .models import Booking, TempBooking
from .views import Room_details_view
import logging



logger = logging.getLogger(__name__)

@receiver(valid_ipn_received)
def valid_ipn_signal(sender, **kwargs):
    ipn = sender
    if ipn.payment_status == ST_PP_COMPLETED:
        try:
            temp_booking = TempBooking.objects.get(id=ipn.invoice)
            booking = Booking.objects.create(
                user=temp_booking.user,
                appart=temp_booking.appart,
                date_enter=temp_booking.date_enter,
                date_out=temp_booking.date_out,
                total=temp_booking.total,
            )
            Room_details_view().complete_booking(booking, temp_booking.appart, {
                'check_in': temp_booking.date_enter,
                'check_out': temp_booking.date_out,
            })
            temp_booking.is_paid = True
            temp_booking.save()
            logger.info(f"Booking completed and saved: {booking.id}")
        except TempBooking.DoesNotExist:
            logger.error(f"TempBooking with id {ipn.invoice} does not exist.")
        except Exception as e:
            logger.error(f"Error processing IPN: {e}")


@receiver(invalid_ipn_received)
def invalid_ipn_signal(sender,**kwargs):
    ipn = sender
    if ipn.payment_status == ST_PP_COMPLETED:
        try:
            temp_booking = TempBooking.objects.get(id=ipn.invoice)
            booking = Booking.objects.create(
                user=temp_booking.user,
                appart=temp_booking.appart,
                date_enter=temp_booking.date_enter,
                date_out=temp_booking.date_out,
                total=temp_booking.total,
            )
            Room_details_view().complete_booking(booking, temp_booking.appart, {
                'check_in': temp_booking.date_enter,
                'check_out': temp_booking.date_out,
            })
            temp_booking.is_paid = True
            temp_booking.save()
            logger.info(f"Booking completed and saved: {booking.id}")
        except TempBooking.DoesNotExist:
            logger.error(f"TempBooking with id {ipn.invoice} does not exist.")
        except Exception as e:
            logger.error(f"Error processing IPN: {e}")