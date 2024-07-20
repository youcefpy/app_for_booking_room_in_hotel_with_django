
from django.contrib import admin
from django.urls import path,include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls'),name="accounts"),
    path('',include('bookingApp.urls')),
]
