from django.shortcuts import render,redirect,get_object_or_404
from django_hosts.resolvers import reverse
from django.contrib import  messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone 
from datetime import timedelta

from account.models import Account,PurchaseCoupon,RefferalProfile

from .models import Withdrawal



login_url = reverse('loginpage', host="account")



def get_deadline(remaining_days):
	return timezone.now() + timedelta(days=remaining_days)


def calculate(perc,amount):
    perc = (amount/perc) * 100
    return perc + amount

def daily_calculate(perc,amount):
    perc = (amount/perc) * 100
    return perc 


@login_required(login_url=login_url)
def dashboard_view(request):
    if request.user.is_expired == True:
        messages.success(request, f'Subscription Ended')
        return render(request, 'dashboard.html')
    else:
        return render(request, 'dashboard.html')



@login_required(login_url=login_url)
def refferal_view(request):
    myrecs = get_object_or_404(RefferalProfile, user=request.user)
    return render(request, 'refferal.html',{'myrecs':myrecs})



@login_required(login_url=login_url)
def mine_view(request):
    return render(request, 'mine.html')


@login_required(login_url=login_url)
def renew_investment_view(request):
    user = request.user
    if request.POST:
        code = request.POST.get('code')
        try:
            coupon = PurchaseCoupon.objects.get(code=code)
        except PurchaseCoupon.DoesNotExist:
            messages.success(request, f'Invalid Code')
            return redirect('renew_sub')
        if coupon.is_active == False:
            messages.success(request, f'This Code Has Already been Used Or Invalid')
            return redirect('renew_sub')
        else:
            coupon.is_active = False
            coupon.save()
            user.end_date = get_deadline(2)
            user.next_earnings = get_deadline(1) 
            user.code = coupon
            user.is_expired = False
            user.save()
            messages.success(request, f'Subscription Renewed')
            return redirect('userpage')
    else:
        if request.user.is_expired == False:
            messages.success(request, f'Ongoin Subscription')
            return redirect('userpage')
        else:
            return render(request, 'renew_investment.html')





@login_required(login_url=login_url)
def history_view(request):
    withdrawals = Withdrawal.objects.all().order_by('-date')
    return render(request, 'history.html',{"withdrawals":withdrawals})

@login_required(login_url=login_url)
def withdrawal_view(request):
    user = request.user
    if request.POST:
        amount = int(request.POST.get('amount'))
        account_name =  request.POST.get('account_name')
        account_number = request.POST.get('account_number')
        bank =  request.POST.get('bank')
        balance_type =  request.POST.get('balance_type')
        if balance_type == "main_balance":
            if amount > user.balance:
                messages.success(request, 'Inssuficient Funds In Your Main Balance')
                return redirect('withdraw')
            else:
                Withdrawal.objects.create(
                    user=user,amount=amount,account_number=account_number,
                    account_name=account_name,bank=bank,
                    balance_type=balance_type)
                user.balance -= amount
                user.save()
                messages.success(request, 'Withdraw Order Placed You Will Be Notify Once It Has Been Approved')
                return redirect('withdraw')
        elif balance_type == "referral_balance":
            if amount > user.bonus:
                messages.success(request, 'Inssuficient Funds In Your Refferal Balance')
                return redirect('withdraw')
            else:
                Withdrawal.objects.create(
                    user=user,amount=amount,account_number=account_number,
                    account_name=account_name,bank=bank,
                    balance_type=balance_type)
                user.bonus -= amount
                user.save()
                messages.success(request, 'Withdraw Order Placed You Will Be Notify Once It Has Been Approved')
                return redirect('withdraw')
        else:
            messages.success(request, 'UNKNOWN ERROR OCCURED')
            return redirect('withdraw')
    return render(request, 'withdrawal.html')




def user_daily_income(request):
    user = request.user
    if request.POST:
        if user.is_expired == True:
            return JsonResponse({"msg":'Unknown Error Occured'})
        else:
            if user.days == 2:
                user.is_expired = True
                user.balance += calculate(15,int(user.code.price))
                user.save()
                return JsonResponse({"msg":'Subscription Ended'})
            else:
                user.days += 1
                remaining_days = int(user.days)
                user.next_earnings =  get_deadline(1)
                user.balance += daily_calculate(15,int(user.code.price))
                user.save()
                return JsonResponse({"msg":'Account Credited'})
    else:
        return JsonResponse({"msg":'Unknown Error Occured'})

