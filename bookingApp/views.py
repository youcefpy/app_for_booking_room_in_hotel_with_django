
import os
from django.conf import settings
from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from .models import Booking, Appartment,Contact
from .forms import AvailabilityForm,ContactForm
from django.views.generic import ListView,FormView,View
from .booking_function import availability
from django.contrib import messages

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

from threading import Timer
from django.utils import timezone
from django.templatetags.static import static

from django.template.loader import get_template
from xhtml2pdf import pisa


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


def search_appartement_state(request):
    state = request.POST.get('state','')
    apparts = Appartment.objects.filter(state__icontains=state)
    context ={
        'serach_apparts':apparts,
    }
    return render(request,'search_apparts.html',context)



def delete_booking(request,id_booking):

    if request.user.is_staff : 
        del_booking = Booking.objects.get(id=id_booking)
        del_booking.appart.is_available = True
        del_booking.appart.save()
        del_booking.delete()

    else : 
        del_booking = Booking.objects.get(id=id_booking)
        del_booking.appart.is_available = True
        del_booking.appart.save()
        del_booking.delete()

    return redirect("booking_list")



def contact(request):

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            f_name = form['first_name'].value()
            l_name = form['last_name'].value()
            email = form['email'].value()
            message = form['message'].value()
            contact = Contact.objects.create(
                first_name = f_name,
                last_name = l_name,
                email = email,
                message = message,
            )
            contact.save()
            messages.success(request,"Your Message was send with success")
            return redirect("index")
        
        else : 
            messages.error(request, "There was an error. Please try again.")
    else : 
        form = ContactForm()

    context ={
        'form' : ContactForm()
    }

    return render(request,'contact.html',context)



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
            if self.request.user.is_authenticated : 

                if len(availabale_apprts)>0 : 
                    appart = availabale_apprts[0]
                    num_days = (data['check_out'] - data['check_in']).days
                    total_const_appart = appart.price_per_night * num_days
                    # print(f"number of days for booking the appartment : {num_days} ")
                    # print(f"total cost for booking the appartement is : {total_const_appart} DA")

                    booking = Booking.objects.create(
                        user = self.request.user,
                        appart = appart,
                        date_enter = data['check_in'],
                        date_out = data['check_out'],
                        total = total_const_appart,   
                    )

                    booking.save()
                    #after booking let's make availability to false
                    appart.is_available = False
                    appart.save()
                    #reset the availability to true after the delay of booking 
                    now = timezone.now()
                    check_out = data['check_out']
                    if check_out.tzinfo is None:
                        check_out = timezone.make_aware(check_out, timezone.get_current_timezone())
                    time_is_sec = (check_out - now).total_seconds()       
                    Timer(time_is_sec,self.reset_availability,[appart.id]).start()

                    return render(request,'validation_booking.html',{'booking':booking})
                else : 
                    return HttpResponse(f"this appartement is not available from {data['check_in']} to {data["check_out"]} ")
            else : 
                messages.warning(request,'You should login before book, Please login and after you book :)')
                return redirect('account_login')
        else : 
            context={
                'appart_id':appartement,
                'form':form,
            }
            return render(request,"appart_details.html",context)
        

    def reset_availability(self, appart_id):
        appart = Appartment.objects.get(id=appart_id)
        appart.is_available = True
        appart.save()




def gen_pdf(request,booking_id):
    booking = get_object_or_404(Booking,id=booking_id)
    user = request.user
    template_path = 'pdf_booking.html'
    static_url = request.build_absolute_uri(static('')).rstrip('/') + '/'
    context = {
        'booking': booking,
        'user':user,
        'static_url':static_url,
        }
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="booking_{}.pdf"'.format(booking.id)

    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response



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



