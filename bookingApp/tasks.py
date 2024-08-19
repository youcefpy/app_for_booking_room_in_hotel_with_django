import logging
from celery import shared_task
from django.utils import timezone
from .models import Booking
import pytz 


logger = logging.getLogger(__name__)

@shared_task
def reset_availability():
    try:
        
        paris_tz = pytz.timezone('Europe/Paris')
        today = timezone.now().astimezone(paris_tz)

        logger.info(f"Task reset_availability started at {today}")
        
        bookings = Booking.objects.filter(date_out__lt=today, room__is_available=False)
        logger.info(f"Found {bookings.count()} bookings to process.")

        for booking in bookings:
            room = booking.room
            room.is_available = True
            room.save()
            logger.info(f"Room {room.id} availability reset to True after {booking.date_out}.")
        logger.info("Task reset_availability completed successfully.")
    except Exception as e:
        logger.error(f"Error in reset_availability task: {e}")