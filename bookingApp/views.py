from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from .models import Booking, Appartment
from .forms import AvailabilityForm
from django.views.generic import ListView,FormView,View
from .booking_function import availability
# Create your views here.


def index(request):
    appartment = Appartment.objects.all()
    context={
        'appartement': appartment,
    }
    return render(request,'index.html',context)



def booking_list(request):   
    if request.user.is_staff : 
        booking_list = Booking.objects.all()
        
        
    else : 
        booking_list = Booking.objects.filter(user = request.user)
    
    context={
        'booking_list':booking_list,
    }

    return render(request,"booking_list.html",context)
    

class AppartListView(ListView):
    model = Appartment


# def appart_details(request,id:int):
#     appart_id = get_object_or_404(Appartment,id=id)
#     context={
#         'appart_id':appart_id,
#     }

#     return render(request,'appart_details.html',context)


class Appartement_details_view(View):
    def get(self,request,*args,**kwargs):
        appart_id = self.kwargs.get('id',None)
        appartement =get_object_or_404(Appartment,id=appart_id)
        form = AvailabilityForm()
        if appartement : 

            context={
                'appart_id':appartement,
                'form':form,
            }
            return render(request,"appart_details.html",context)
        else : 
            return HttpResponse("the appartement does not exist ! ")

    def post(self,request,*args,**kwargs):
        appart_id = self.kwargs.get('id',None)
        appart_list = Appartment.objects.filter(id=appart_id)
        availabale_apprts = []
        form = AvailabilityForm(request.POST)
        appartement =get_object_or_404(Appartment,id=appart_id)
        if form.is_valid():
            data = form.cleaned_data
            for appart in appart_list : 
                if availability.booking_logic(appart, data['check_in'],data['check_out']) :
                    availabale_apprts.append(appart)

            if len(availabale_apprts)>0 : 
                appart = availabale_apprts[0]
                num_days = (data['check_out'] - data['check_in']).days
                total_const_appart = appart.price_per_night * num_days
                print(f"number of days for booking the appartment : {num_days} ")
                print(f"total cost for booking the appartement is : {total_const_appart} DA")
                booking = Booking.objects.create(
                    user = self.request.user,
                    appart = appart,
                    date_enter = data['check_in'],
                    date_out = data['check_out'],
                    total = total_const_appart

                )
                booking.save()
                return HttpResponse(f"Booking confirmed: {booking}")
            else : 
                return HttpResponse("There is no available appartement ! ")
        else : 
            context={
                'appart_id':appartement,
                'form':form,
            }
            return render(request,"appart_details.html",context)

class Booking_view(FormView):

    form_class = AvailabilityForm
    template_name = 'booking.html'

    def form_valid(self, form):
        data = form.cleaned_data
        appart_list = Appartment.objects.all()
        availabale_apprts = []
        for appart in appart_list : 
            if availability.booking_logic(appart, data['check_in'],data['check_out']) :
                availabale_apprts.append(appart)

        if len(availabale_apprts)>0 : 
            appart = availabale_apprts[0]
            booking = Booking.objects.create(
                user = self.request.user,
                appart = appart,
                date_enter = data['check_in'],
                date_out = data['check_out'],
            )
            booking.save()
            return HttpResponse(booking)
        else : 
            return HttpResponse("There is no available appartement ! ")



