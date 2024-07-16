from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.


class Appartment(models.Model):
    space = models.DecimalField(max_digits=10,decimal_places=2)
    beds = models.IntegerField(default=1)
    address = models.CharField(max_length=1000)
    state= models.CharField(max_length=255)
    bath = models.IntegerField(default=1) 
    description = models.TextField(max_length=10000,blank=True)
    image_appart = models.ImageField(upload_to='media')
    price_per_night = models.DecimalField(max_digits=10,decimal_places=2,null=False)
    def __str__(self):
        return f'{self.state} {self.space} m2, beds : {self.beds}'



class Booking(models.Model):

    user= models.ForeignKey(User,on_delete=models.CASCADE)
    appart = models.ForeignKey(Appartment,on_delete=models.CASCADE)
    date_enter = models.DateTimeField(blank=True)
    date_out = models.DateTimeField(blank=True)
    total = models.DecimalField(max_digits=10,decimal_places=2)
        
    # def total(self):
    #     return self.appart.price_per_night * (self.date_out-self.date_enter)

    def __str__(self):
        return f"{self.user} book appart in {self.appart.state} \n {self.appart.price_per_night} DA \n date_in {self.date_enter} \nand the date of out is {self.date_out} \n and the total for the stay is : {self.total} DA"

    
    
