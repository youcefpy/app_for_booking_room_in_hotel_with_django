from django.urls import path
from .views import index,Booking_view,Appartement_details_view,booking_list
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',index,name='index'),
    path('booking/',Booking_view.as_view(),name='Booking_view'),
    path('booking_list/',booking_list,name='booking_list'),
    path('AppartDetails/<int:id>',Appartement_details_view.as_view(),name='appartDetails'),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL,document_root=settings.STATICFILES_DIRS)