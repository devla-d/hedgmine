from django import forms
from django.contrib.auth  import login,authenticate,logout
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError


from .models import Account,PurchaseCoupon


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    fullname = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder':"Fullname"
            }
        ),
        label = '',
        required=True
    )
    email = forms.EmailField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'type': 'email',
                'class': 'form-control',
                'placeholder':"Email"
            }
        ),
        label = '',
        required=True
    )
    password1 = forms.CharField(max_length=30, min_length=6,label='', widget=forms.PasswordInput(attrs={'placeholder': "PASSWORD", 'class': 'form-control',}) ,required=True)
    #password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    coupon = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder':"Coupon"
            }
        ),
        label = '',
        required=True
    )
    phone = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'tel',
                'class': 'form-control',
                'placeholder':'Phone number',
                 'pattern':"[0-9]{3}-[0-9]{3}-[0-9]{4}"
            }
        ),
        label = "",
         required=True
    )

    class Meta:
        model = Account
        fields = ('fullname', 'email','phone','password1','coupon')

    '''def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2'''

    def clean(self):
        coupon = self.cleaned_data['coupon']
        try:
            code = PurchaseCoupon.objects.get(code=coupon)
        except PurchaseCoupon.DoesNotExist:
            raise forms.ValidationError("Invalid Code")
        if code.is_active == False:
            raise forms.ValidationError("Code Is Expired")


    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        code = self.cleaned_data['coupon']
        c = PurchaseCoupon.objects.get(code=code)
        c.is_active = False
        user.code = c
        c.save()
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Account
        fields = ('email', 'password', 'date_of_birth', 'is_active', 'is_staff')






class LoginForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(max_length=30, min_length=4,label='', widget=forms.PasswordInput(attrs={'placeholder': "PASSWORD", 'class': 'form-control',}) ,required=True)

    phone = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'tel',
                'class': 'form-control',
                'placeholder':'Phone number',
                 'pattern':"[0-9]{3}-[0-9]{3}-[0-9]{4}"
            }
        ),
        label = "",
         required=True
    )

    class Meta:
        model = Account
        fields = ('phone','password1')


    def clean(self):
        if self.is_valid():
            phone = self.cleaned_data['phone']
            password =  self.cleaned_data['password1']
            if not authenticate(phone=phone,password=password):
                raise forms.ValidationError('Invalid Credentials')





class ProfileForm(forms.ModelForm):


    date_of_birth = forms.DateTimeField(
            widget=forms.TextInput(
                attrs={
                    'type': 'date',
                     'class': 'form-control custom-date',
                }
            ),
             label = '',
            required=True)

    class Meta:
        model = Account
        fields = ('fullname','username','email', 'date_of_birth', 'occupation', 'home_address')