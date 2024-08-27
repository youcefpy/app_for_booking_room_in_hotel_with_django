from django.conf import settings
from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from .models import Booking, Room,Contact,TempBooking,CommentRoom,Category
from .forms import AvailabilityForm,ContactForm,PaymentMethodForm,CustomPayPalPaymentsForm,CommentRoomForm,SeachAvailableRoom
from django.urls import reverse
from django.views.generic import ListView,FormView,View
from .booking_function import availability
from django.contrib import messages


from django.templatetags.static import static

from django.template.loader import get_template
from xhtml2pdf import pisa


from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from datetime import datetime
from django.utils import timezone
import pytz

# Create your views here.



def index(request):
    room = Room.objects.all()
    categories = Category.objects.all()

    context={
        'category':categories,
        'rooms': room,
    }
    return render(request,'index.html',context)


def list_rooms(request):
    room = Room.objects.all()

    context={
        'rooms':room
    }

    return render(request,'rooms.html',context)


def booking_list(request):   
    if request.user.is_staff : 
        booking_list = Booking.objects.all()
        
        
    else : 
        booking_list = Booking.objects.filter(user = request.user)
    
    
    paris_tz = pytz.timezone('Europe/Paris')
    today = timezone.now().astimezone(paris_tz)
    context={
        'booking_list':booking_list,
        'now':today
    }

    return render(request,"booking_list.html",context)

def search_room_category(request,category):
    cat_room = Room.objects.filter(category_room__name_category__icontains=category)
    context={
        'categories_room':cat_room,
        'category_name':category,
    }
    return render(request,'search_rooms.html',context)



def delete_booking(request,id_booking):

    if request.user.is_staff : 
        del_booking = Booking.objects.get(id=id_booking)
        del_booking.room.is_available = True
        del_booking.room.save()
        del_booking.delete()

    else : 
        del_booking = Booking.objects.get(id=id_booking)
        del_booking.room.is_available = True
        del_booking.room.save()
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



class RoomListView(ListView):
    model = Room


# def appart_details(request,id:int):
#     appart_id = get_object_or_404(Appartment,id=id)
#     context={
#         'appart_id':appart_id,
#     }

#     return render(request,'appart_details.html',context)


class Room_details_view(View):
    def get(self, request, *args, **kwargs):
        room_id = self.kwargs.get('id', None)
        room = get_object_or_404(Room, id=room_id)
        comments = CommentRoom.objects.filter(room = room)
        form = AvailabilityForm()

        formComment = CommentRoomForm()

        if room:
            context = {
                'room_id': room,
                'form': form,
                'comments':comments,
                'formComment' : formComment,

            }
            return render(request, "room_details.html", context)
        else:
            return HttpResponse("The Room does not exist!")

    def post(self, request, *args, **kwargs):
        room_id = self.kwargs.get('id', None)
        room_list = Room.objects.filter(id=room_id)
        available_room = []
        form = AvailabilityForm(request.POST)
        payment_method_form = PaymentMethodForm(request.POST)

        formComment = CommentRoomForm(request.POST)
        room = get_object_or_404(Room, id=room_id)
        if formComment.is_valid():
            comment = formComment.save(commit=False)
            comment.user = self.request.user
            comment.room= room 
            comment.save()
            return redirect('roomDetails',id=room_id)

        if form.is_valid() and payment_method_form.is_valid():
            payment_method_chose = payment_method_form.cleaned_data['payment_method']
            data = form.cleaned_data
    
            for room in room_list:
                if availability.booking_logic(room, data['check_in'], data['check_out']):
                    available_room.append(room)


            paris_tz = pytz.timezone('Europe/Paris')
            today = timezone.now().astimezone(paris_tz)

            name = data['name']
            phone_number = data['phone_number']
            check_in = data['check_in']
            check_out = data['check_out']

            print(f'check_in : {check_in.month}')
            print(f'check out : {check_out.month}')
            print(f'today : {today}')

            if self.request.user.is_authenticated:  

                if check_out < check_in:
                    return HttpResponse('Invalid Booking, The Date in should be less then the Date out, So please try again.')
                
                if check_in < today or check_out < today:
                    return HttpResponse('Invalid Booking, Date In and Date Out should be greater than or equal to today. Please try again.')


                if len(available_room) > 0:
                    room = available_room[0]
                    num_days = (data['check_out'] - data['check_in']).days
                    total_cost_room = room.price_per_night * num_days

                    if payment_method_chose == 'pay_on_hotel':
                        booking = Booking.objects.create(
                            user=self.request.user,
                            room=room,
                            name=name,
                            phone_number = (phone_number),
                            date_enter=data['check_in'],
                            date_out=data['check_out'],
                            total=total_cost_room,
                        )
                        self.complete_booking(booking, room)
                        
                        return render(request, 'validation_booking.html', {'booking': booking})
                    else:
                        temp_booking = TempBooking.objects.create(
                            user=self.request.user,
                            room=room,
                            name=name,
                            phone_number =(phone_number),
                            date_enter=data['check_in'],
                            date_out=data['check_out'],
                            total=total_cost_room,
                        )
                        total_amount_for_booking = temp_booking.total / 220
                        total_amount_for_booking_in_usd = str(total_amount_for_booking)
                        host = request.get_host()
                        paypal_dict = {
                            "business": settings.PAYPAL_RECEIVER_EMAIL,
                            "amount": total_amount_for_booking_in_usd,
                            "item_name": f"room_id : {temp_booking.room.id}",
                            "invoice": str(temp_booking.id),
                            'currency_code': 'USD',
                            "notify_url": f'http://{host}{reverse("paypal-ipn")}',
                            "return": f'http://{host}{reverse("payment_success", args=[temp_booking.id])}',
                            "cancel_return": f'http://{host}{reverse("index")}',
                        }
                        form = CustomPayPalPaymentsForm(initial=paypal_dict)
                        context = {
                            "form_paypal": form,
                            "booking": temp_booking,
                            'formComment':formComment,
                        }
                        return render(request, "paypal-payment.html", context)
                else:
                    return HttpResponse(f"This room is not available from {data['check_in']} to {data['check_out']}.")
            else:
                messages.warning(request, 'You should login before booking. Please login and then book.')
                return redirect('account_login')
        else:
   
            context = {
                'room_id': room_id,
                'form': form,
                'payment_method_form': payment_method_form,
                'formComment' : formComment,

            }
            return render(request, "room_details.html", context)

    def complete_booking(self, booking, room):
        booking.save()
        room.is_available = False
        print(f'room avivalability : {room.is_available}')
        room.save()

        
def list_free_booking_room(request):
    if request.method == 'POST':
        form = SeachAvailableRoom(request.POST)
        if not form.is_valid():
            print(form.errors)
            print('Raw POST data:', request.POST)
        if form.is_valid():
            data = form.cleaned_data
            adult = data['adult']
            child = data['child']
            check_in = data['check_in']
            check_out = data['check_out']
            
            list_available_rooms = []
            rooms = Room.objects.filter(adult=adult,child=child)
            for room in rooms:
                if availability.booking_logic(room,check_in,check_out):
                    list_available_rooms.append(room)
            print(list_available_rooms)
            context={
                'form':form,
                'list_available_rooms':list_available_rooms,
            }
            print('if is executed')
            return render(request,'serach_free_booking_room.html',context)
            
        else : 
            form = SeachAvailableRoom()
            print(form.errors)
            context={
                'form':form,
            }
            print('else is executed')
            return render(request,'serach_free_booking_room.html',context)
        


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
                room=temp_booking.room,
                name= temp_booking.name,
                phone_number=(temp_booking.phone_number),
                date_enter=temp_booking.date_enter,
                date_out=temp_booking.date_out,
                total=temp_booking.total,
                is_paied = True
            )
            Room_details_view().complete_booking(booking, temp_booking.room)
            temp_booking.is_paid = True
            temp_booking.save()

        return render(request, 'success_payment.html', {'booking': booking})

    def post(self, request, temp_booking_id):
        temp_booking = get_object_or_404(TempBooking, id=temp_booking_id)

        if not temp_booking.is_paid:
            booking = Booking.objects.create(
                user=temp_booking.user,
                room=temp_booking.room,
                name= temp_booking.name,
                phone_number=(temp_booking.phone_number),
                date_enter=temp_booking.date_enter,
                date_out=temp_booking.date_out,
                total=temp_booking.total,
                is_paied = True
            )
            Room_details_view().complete_booking(booking, temp_booking.room)
            temp_booking.is_paid = True
            temp_booking.save()

        return render(request, 'success_payment.html', {'booking': booking})

class Booking_view(FormView):

    form_class = AvailabilityForm
    template_name = 'booking.html'

    def form_valid(self, form):
        data = form.cleaned_data
        room_list = Room.objects.all()
        availabale_apprts = []
        for room in room_list : 
            if availability.booking_logic(room, data['check_in'],data['check_out']) :
                availabale_apprts.append(room)

        if len(availabale_apprts)>0 : 
            room = availabale_apprts[0]
            booking = Booking.objects.create(
                user = self.request.user,
                room = room,
                date_enter = data['check_in'],
                date_out = data['check_out'],
            )
            booking.save()
            return HttpResponse(booking)
        else : 
            return HttpResponse("There is no available room ! ")
        



