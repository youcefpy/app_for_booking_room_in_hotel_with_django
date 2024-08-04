
import os
from uuid import uuid4 
from django.conf import settings
from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from .models import Booking, Appartment,Contact,TempBooking
from .forms import AvailabilityForm,ContactForm,PaymentMethodForm
from django.urls import reverse
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

from paypal.standard.forms import PayPalPaymentsForm

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from datetime import datetime, timedelta
from django.utils import timezone

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
    def get(self, request, *args, **kwargs):
        appart_id = self.kwargs.get('id', None)
        appartement = get_object_or_404(Appartment, id=appart_id)
        
        form = AvailabilityForm()
        if appartement:
            context = {
                'appart_id': appartement,
                'form': form,
            }
            return render(request, "appart_details.html", context)
        else:
            return HttpResponse("The appartement does not exist!")

    def post(self, request, *args, **kwargs):
        appart_id = self.kwargs.get('id', None)
        appart_list = Appartment.objects.filter(id=appart_id)
        available_aparts = []
        form = AvailabilityForm(request.POST)
        payment_method_form = PaymentMethodForm(request.POST)

        if form.is_valid() and payment_method_form.is_valid():
            appartement = get_object_or_404(Appartment, id=appart_id)
            payment_method_chose = payment_method_form.cleaned_data['payment_method']
            data = form.cleaned_data

            for appart in appart_list:
                if availability.booking_logic(appart, data['check_in'], data['check_out']):
                    available_aparts.append(appart)

            if self.request.user.is_authenticated:
                if len(available_aparts) > 0:
                    appart = available_aparts[0]
                    num_days = (data['check_out'] - data['check_in']).days
                    total_cost_appart = appart.price_per_night * num_days

                    if payment_method_chose == 'pay_on_hotel':
                        booking = Booking.objects.create(
                            user=self.request.user,
                            appart=appart,
                            date_enter=data['check_in'],
                            date_out=data['check_out'],
                            total=total_cost_appart,
                        )
                        self.complete_booking(booking, appart, data)
                        return render(request, 'validation_booking.html', {'booking': booking})
                    else:
                        temp_booking = TempBooking.objects.create(
                            user=self.request.user,
                            appart=appart,
                            date_enter=data['check_in'],
                            date_out=data['check_out'],
                            total=total_cost_appart,
                        )
                        total_amount_for_booking = temp_booking.total / 220
                        total_amount_for_booking_in_usd = str(total_amount_for_booking)
                        host = request.get_host()
                        paypal_dict = {
                            "business": settings.PAYPAL_RECEIVER_EMAIL,
                            "amount": total_amount_for_booking_in_usd,
                            "item_name": f"appart_state : {temp_booking.appart.state}, appart_id : {temp_booking.appart.id}",
                            "invoice": str(temp_booking.id),
                            'currency_code': 'USD',
                            "notify_url": f'http://{host}{reverse("paypal-ipn")}',
                            "return": f'http://{host}{reverse("payment_success", args=[temp_booking.id])}',
                            "cancel_return": f'http://{host}{reverse("index")}',
                        }
                        form = PayPalPaymentsForm(initial=paypal_dict)
                        context = {
                            "form_paypal": form,
                            "booking": temp_booking,
                        }
                        return render(request, "paypal-payment.html", context)
                else:
                    return HttpResponse(f"This appartement is not available from {data['check_in']} to {data['check_out']}.")
            else:
                messages.warning(request, 'You should login before booking. Please login and then book.')
                return redirect('account_login')
        else:
            context = {
                'appart_id': appart_id,
                'form': form,
                'payment_method_form': payment_method_form,
            }
            return render(request, "appart_details.html", context)

    def complete_booking(self, booking, appart, data):
        booking.save()
        appart.is_available = False
        appart.save()

        # Convert check_out date to datetime if it is not already
        check_out = data['check_out']
        if isinstance(check_out, datetime):
            check_out_dt = check_out
        else:
            check_out_dt = datetime.combine(check_out, datetime.min.time())
            check_out_dt = timezone.make_aware(check_out_dt, timezone.get_current_timezone())

        now = timezone.now()
        time_is_sec = (check_out_dt - now).total_seconds()
        Timer(time_is_sec, self.reset_availability, [appart.id]).start()

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


# def view_that_asks_for_money(request,booking_id):
#     booking = get_object_or_404(Booking,id=booking_id)
#     total_amount_for_booking = booking.total/220
#     total_amount_for_booking_in_usd = str(total_amount_for_booking)

#     host = request.get_host()
#     paypal_dict = {
#         "business": settings.PAYPAL_RECEIVER_EMAIL,
#         "amount": total_amount_for_booking_in_usd,
#         "item_name": f"appart_state : {booking.appart.state}, appart_id : {booking.appart.id}",
#         "invoice": str(uuid4()),
#         'currency_code': 'USD',
#         "notify_url":  f'http://{host}{reverse('paypal-ipn')}',
#         "return": f'https://{host}{reverse('payment_success')}',
#         "cancel_return": f'https://{host}{(reverse('index'))}',
#         "custom": "premium_plan",  
#     }

#     # Create the instance.
#     form = PayPalPaymentsForm(initial=paypal_dict)
#     context = {
#         "form_paypal": form,
#         "booking":booking,
        
#         }
#     return render(request, "payment.html", context)


@method_decorator(csrf_exempt, name='dispatch')
class PayPalPaymentView(View):
    def get(self, request, temp_booking_id):
        temp_booking = get_object_or_404(TempBooking, id=temp_booking_id)

        if not temp_booking.is_paid:
            booking = Booking.objects.create(
                user=temp_booking.user,
                appart=temp_booking.appart,
                date_enter=temp_booking.date_enter,
                date_out=temp_booking.date_out,
                total=temp_booking.total,
            )
            Appartement_details_view().complete_booking(booking, temp_booking.appart, {
                'check_in': temp_booking.date_enter,
                'check_out': temp_booking.date_out,
            })
            temp_booking.is_paid = True
            temp_booking.save()

        return render(request, 'success_payment.html', {'booking': booking})

    def post(self, request, temp_booking_id):
        temp_booking = get_object_or_404(TempBooking, id=temp_booking_id)

        if not temp_booking.is_paid:
            booking = Booking.objects.create(
                user=temp_booking.user,
                appart=temp_booking.appart,
                date_enter=temp_booking.date_enter,
                date_out=temp_booking.date_out,
                total=temp_booking.total,
            )
            Appartement_details_view().complete_booking(booking, temp_booking.appart, {
                'check_in': temp_booking.date_enter,
                'check_out': temp_booking.date_out,
            })
            temp_booking.is_paid = True
            temp_booking.save()

        return render(request, 'success_payment.html', {'booking': booking})

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



