from django.shortcuts import render,redirect,get_object_or_404
from django_hosts.resolvers import reverse
from django.contrib import  messages




from account.models import Account,PurchaseCoupon


def home_view(request):
    return render(request,"index.html")




def about_view(request):
    return render(request,"about.html")


def contact_view(request):
    return render(request,"contact.html")


def verify_code_view(request):
    if request.POST:
        code = request.POST.get('code')
        try:
            coupon = PurchaseCoupon.objects.get(code=code)
        except PurchaseCoupon.DoesNotExist:
            messages.success(request, f'Invalid Code')
            return redirect('verifycodepage')
        if coupon.is_active == False:
            messages.success(request, f'This Code Has Already been Used Or Invalid')
            return redirect('verifycodepage')
        else:
            messages.success(request, f'Valid Code')
            return redirect('verifycodepage')
    return render(request,"verify-pin.html")



def vendors_view(request):
    return render(request,"vendors.html")






def handler404(request, exception):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)