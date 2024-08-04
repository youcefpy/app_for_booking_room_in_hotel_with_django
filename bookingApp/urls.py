from django.urls import path
from .views import index,Booking_view,Appartement_details_view,booking_list,delete_booking,contact,search_appartement_state,gen_pdf,PayPalPaymentView
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('',index,name='index'),
    path('booking/',Booking_view.as_view(),name='Booking_view'),
    path('booking_list/',booking_list,name='booking_list'),
    path('AppartDetails/<int:id>',Appartement_details_view.as_view(),name='appartDetails'),
    path('delete_booking/<int:id_booking>',delete_booking,name='delete_booking'),
    path("services/",TemplateView.as_view(template_name='services.html'),name='services'),
    path("about/",TemplateView.as_view(template_name='about.html'),name='about'),
    path('conatct/',contact,name="contact"),
    path('search_appart/', search_appartement_state, name='search_appart'),
    path('gen_pdf/<int:booking_id>/',gen_pdf,name="gen_pdf"),
    path('paypal_payment/<int:temp_booking_id>/',PayPalPaymentView.as_view(),name="payment_success")
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL,document_root=settings.STATICFILES_DIRS)