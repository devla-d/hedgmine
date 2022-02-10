from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField



from account.models import Account

from user_dashboard.models import Withdrawal




class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
 
    class Meta:
        model = Account
        fields ="__all__"




class WithdrawChangeForm(forms.ModelForm): 
    '''approved_date = forms.DateTimeField(
            widget=forms.TextInput(
                attrs={
                    'type': 'date',
                     'class': 'form-control custom-date',
                }
            ),
             label = 'App',
            required=True)'''
 
    class Meta:
        model = Withdrawal
        fields ="__all__"