from django.shortcuts import render,redirect,get_object_or_404
from django_hosts.resolvers import reverse
from django.contrib import  messages
from django.contrib.auth  import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import  timedelta



from .models import Account,PurchaseCoupon,RefferalProfile
from .forms import UserCreationForm,LoginForm,ProfileForm



#login_url = reverse('loginpage', host="account")


def calculate_perc():
    return 100000

def get_deadline():
	return timezone.now() + timedelta(days=1)

def register_view(request):
    if request.POST:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            if request.POST.get('refferd_by'):
                refferd_by_username = str(request.POST.get('refferd_by'))
                print(refferd_by_username)
                try:
                    refferd_by_user = Account.objects.get(username=refferd_by_username)
                    space_username = str(form.cleaned_data['fullname'])
                    username = space_username.replace(" ","_")
                    instance.username = username
                    instance.next_earnings = get_deadline()
                    instance.save()
                    new_user_ref =  RefferalProfile.objects.create(user=instance)
                    new_user_ref.recommended_by = refferd_by_user
                    old_user_ref = RefferalProfile.objects.get(user =refferd_by_user)
                    old_user_ref.recomended_users.add(instance)
                    old_user_ref.user.refferal += 1
                    old_user_ref.user.bonus += calculate_perc()
                    old_user_ref.save()
                    old_user_ref.user.save()
                    new_user_ref.save()
                    messages.success(request, f'Account created Please Login !')
                    return redirect('loginpage')
                except:
                    messages.info(request, f'Something went Wrong')
                    return redirect('registerpage')
            else:
                
                space_username = str(form.cleaned_data['fullname'])
                username = space_username.replace(" ","_")
                instance.username = username
                instance.next_earnings = get_deadline()
                instance.save()
                RefferalProfile.objects.create(user =instance)
                messages.success(request, f'Account created Please Login !')
                return redirect('loginpage')
    else:
        form = UserCreationForm()
    if request.GET.get('refferal-by'):
        refferd_by = request.GET.get('refferal-by')
        return render(request, 'auth/register.html',{"form":form , "refferd_by" : refferd_by})
    else:
        return render(request, 'auth/register.html',{"form":form})


def login_view(request):
    next_url = get_redirect_if_exists(request)
    destination = reverse('userpage', host="dashboard")
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            phone = request.POST['phone']
            password = request.POST['password1']
            destination = request.POST['destination']
            next_riderect = request.POST.get('next_url')
            user = authenticate(phone=phone, password=password)
            if user:
                login(request,user)
                if next_riderect:
                    return redirect(next_riderect)
                else:
                    return redirect(destination)
    else:
        form = LoginForm()
    return render(request, 'auth/login.html',{"form":form, "destination": destination,'next_url':next_url})





def get_redirect_if_exists(request):
	redirect = None
	if request.GET:
		if request.GET.get("next"):
			redirect = str(request.GET.get("next"))
	return redirect


def logout_view(request):
    logout(request)
    return redirect('loginpage')




@login_required(login_url='/sign-in')
def account_view(request):
    user = request.user
    if request.POST:
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Account Updated!')
            return redirect('accountpage')
    else:
        form = ProfileForm(instance=user)
    return render(request, 'account.html',{"form":form})