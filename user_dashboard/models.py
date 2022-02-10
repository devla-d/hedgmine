from django.db import models



from account.models import Account




class Withdrawal(models.Model):
    user =  models.ForeignKey(Account,related_name='user_withdrawal', on_delete=models.CASCADE)
    amount = models.IntegerField( blank=True,null=True)
    date = models.DateTimeField(auto_now_add=True) 
    approved_date = models.DateTimeField(blank=True,null=True) 
    is_approved = models.BooleanField(default=False)
    status = models.CharField(max_length=40,default="pending")
    account_name = models.CharField(max_length=100) 
    account_number = models.CharField(max_length=40) 
    bank = models.CharField(max_length=40)
    balance_type = models.CharField(max_length=40) 



    def __str__(self):
        return f"{self.user.username}"

