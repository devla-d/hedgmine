
from django.shortcuts import render,redirect,get_object_or_404
from django_hosts.resolvers import reverse
from django.core.mail import EmailMessage, send_mail
from django.contrib import  messages
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from django.template.loader import render_to_string

import string
from uuid import uuid4

from account.models import Account,PurchaseCoupon
from user_dashboard.models import Withdrawal



from .decorators import  manager_required


from .forms import UserChangeForm,WithdrawChangeForm

def unique_id():
    code = str(uuid4()).replace('-','').upper()[:8]
    #code_upper = code
    return code


login_url = reverse('loginpage', host="account")


@manager_required(login_url=login_url)
def dashboard_view(request):
    total_earn = 0
    for i in PurchaseCoupon.objects.filter(is_active=False):
        total_earn += i.price
    context = {
        "earning" : total_earn,
        'users' : Account.objects.all().count(),
        'pending_request': Withdrawal.objects.filter(status="pending").count(),
        'total_withdrawal':Withdrawal.objects.all().count()
    }
    return render(request, 'superuser/dashboard.html',context)


@manager_required(login_url=login_url)
def users_view(request):
    users = Account.objects.all()
    return render(request, 'superuser/users.html',{"users":users})


@manager_required(login_url=login_url)
def user_detail_view(request, pk):
    account = get_object_or_404(Account,pk=pk)
    if request.POST:
        submit = request.POST.get('submit')
        if submit == 'Update':
            form = UserChangeForm(request.POST,instance=account)
            if form.is_valid():
                form.save()
                messages.success(request, ('Account Updated'))
                return redirect(f'/user/{account.id}/')
        elif submit == 'Delete':
            account.delete()
            messages.success(request, ('Account Deleted'))
            return redirect('users')
        else:
            messages.success(request, ('Unknown Error Occured'))
            return redirect(f'/user/{account.id}/')
    else:
        form = UserChangeForm(instance=account)
    return render(request, 'superuser/user.html',{"account":account,"form":form})




@manager_required(login_url=login_url)
def withdrawals_view(request):
    withdrawals = Withdrawal.objects.all().order_by('-date')
    return render(request, 'superuser/withdrawals.html',{"withdrawals":withdrawals})




@manager_required(login_url=login_url)
def withdrawal_detail_view(request,pk):
    withdrawal = get_object_or_404(Withdrawal, pk=pk)
    #user = withdrawal.user
    if request.POST:
        #form = WithdrawChangeForm(request.POST,instance=withdrawal)
        submit = request.POST.get('submit')
        if submit == 'Approve':
            withdrawal.is_approved = True
            withdrawal.status = 'approved'
            withdrawal.approved_date = timezone.now()
            withdrawal.user.withdraw_total += withdrawal.amount
            withdrawal.save()
            withdrawal.user.save()
            messages.success(request, ('Withdrawal Approved'))
            return redirect(f'/withdrawal/{withdrawal.id}/')
        elif submit == 'Decline':
            withdrawal.status = 'declined'
            withdrawal.save()
            messages.success(request, ('Withdrawal Declined'))
            return redirect(f'/withdrawal/{withdrawal.id}/')
        else:
            messages.success(request, ('Unknown Error Occured'))
            return redirect(f'/withdrawal/{withdrawal.id}/')
    else:
        form = WithdrawChangeForm(instance=withdrawal)
    return render(request, 'superuser/withdrawal.html',{"withdrawal":withdrawal,'form':form})




@manager_required(login_url=login_url)
def tokens_view(request):
    tokens = PurchaseCoupon.objects.all().order_by('-id')
    return render(request, 'superuser/tokens.html',{'tokens':tokens})




@manager_required(login_url=login_url)
def create_tokens_view(request):
    if request.POST:
        count = int(request.POST.get('count'))
        price = int(request.POST.get('price'))
        for i in range(1,count):
            PurchaseCoupon.objects.create(code=unique_id(),price=price)
        messages.success(request, ('Created'))
        return redirect('/tokens/')
    else:
        return JsonResponse({"msg":"Unknow Error Occured"})