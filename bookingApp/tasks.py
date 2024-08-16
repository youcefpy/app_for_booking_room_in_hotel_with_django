from celery import shared_task
from .models import Room

@shared_task
def reset_availability(room_id):
    room = Room.objects.get(id=room_id)
    room.is_available = True
    room.save()