import random
import json
import string
from uuid import uuid4
from datetime import  timedelta


from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.conf import settings
from django.utils import timezone


from phonenumber_field.modelfields import PhoneNumberField

from .validators import ASCIIUsernameValidator


def unique_id():
    code = str(uuid4()).replace('-','').upper()[:8]
    #code_upper = code
    return code

def get_deadline():
	return timezone.now() + timedelta(days=2)



class PurchaseCoupon(models.Model):
    code  = models.CharField( max_length = 50,default=unique_id())
    is_active = models.BooleanField(default=True)
    price = models.IntegerField(blank=True,null=True) 

    def __str__(self):
        return f"{self.price} {self.is_active}"

 

class Account(AbstractUser):
    login_id = models.CharField( max_length = 50,default=unique_id(), editable=False)
    username = models.CharField(max_length = 50, blank = True, null = True, unique = True)
    email       = models.EmailField(verbose_name='email', max_length=60, unique=True )
    #phone_number = PhoneNumberField( unique = True)
    phone = models.CharField(max_length = 50, blank = True, null = True, unique = True)
    #profile_image = models.ImageField(blank=True, null=True, upload_to='uploads')
    fullname = models.CharField(max_length = 100, blank = True, null = True)
    date_of_birth = models.DateTimeField(blank=True,null=True)
    occupation = models.CharField(max_length = 100, blank = True, null = True)
    home_address = models.CharField(max_length = 100, blank = True, null = True)
    balance = models.IntegerField(default=0, blank=True,null=True)
    withdraw_total = models.IntegerField(default=0, blank=True,null=True)
    purchase_code = models.CharField(max_length = 100, blank = True, null = True)
    code =  models.OneToOneField(PurchaseCoupon, on_delete = models.CASCADE,blank = True, null = True)
    bonus = models.IntegerField(default=0,blank=True,null=True)
    refferal = models.IntegerField(default=0,blank=True,null=True)
    next_earnings = models.DateTimeField(blank=True,null=True)
    end_date = models.DateTimeField(default=get_deadline(), blank=True,null=True)
    is_expired = models.BooleanField(default=False)
    days = models.IntegerField(default=2,blank=True,null=True)

 
    username_validator = ASCIIUsernameValidator()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['username']
    


    def __str__(self):
        return self.email






class RefferalProfile(models.Model):
    user = models.OneToOneField(Account, on_delete = models.CASCADE)
    recommended_by = models.ForeignKey(Account,related_name='recom_user', on_delete=models.CASCADE,null=True, blank=True)
    recomended_users = models.ManyToManyField(Account, related_name='fri',blank=True)
    date = models.DateTimeField(auto_now_add=True)
    bonus = models.IntegerField(default=0,blank=True,null=True)



    def recom_profies(self):
        qs = RefferalProfile.objects.all()
        my_rec = []
        for profile in qs:
            if profile.recommended_by == self.user:
                my_rec.append(profile)
        return my_rec



    def __str__(self):
        return self.user.username