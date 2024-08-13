from django import forms
from django.conf import settings
from .models import CommentRoom
from django.utils.html import format_html
from paypal.standard.forms import PayPalPaymentsForm

class AvailabilityForm(forms.Form):

    # appart_list =forms.ModelChoiceField(queryset=Appartment.objects.all(),empty_label="select_appartement")
    check_in = forms.DateTimeField(required=True,input_formats=['%Y-%m-%d %H:%M'],widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    check_out = forms.DateTimeField(required=True,input_formats=["%Y-%m-%d %H:%M"],widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))


class PaymentMethodForm(forms.Form):
    CHOICES = [('pay_on_hotel','Pay on the Hotel'),('paypal_payment','Pay With paypal')]
    payment_method = forms.CharField(label="method_payment",widget=forms.RadioSelect(choices=CHOICES))

class ContactForm(forms.Form):
    first_name= forms.CharField(max_length=255)
    last_name= forms.CharField(max_length=255)
    email = forms.EmailField(max_length=255)
    message = forms.CharField(widget=forms.Textarea)



class CustomPayPalPaymentsForm(PayPalPaymentsForm):
    def get_image(self):
        return ''  # Return an empty string since we're not using an image
    

    def get_endpoint(self):
        if settings.PAYPAL_TEST:
            return "https://www.sandbox.paypal.com/cgi-bin/webscr"
        return "https://www.paypal.com/cgi-bin/webscr"
    

    def render(self):
        return format_html(
            u"""<form action="{0}" method="post">
                    {1}
                    <button type="submit" class="btn-pay">Pay the booking</button>
                </form>""",
            self.get_endpoint(),
            self.as_p()
        )


class CommentRoomForm(forms.ModelForm):
    class Meta : 
        model = CommentRoom
        fields = ['comment']
        widgets={
            'comment':forms.Textarea(
                attrs={
                    'class':'form-control',
                    'placeholder':'Leave a comment',
                    'id':'commentTextArea'
                    }
                    )
            
        }