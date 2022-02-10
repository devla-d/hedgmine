from django.urls import path


from . import views




urlpatterns = [
    path('',views.dashboard_view, name="userpage"),
    path('my-refferal/',views.refferal_view, name="refferalpage"),
    path('my-minning/',views.mine_view, name="minepage"),
    path('withdraw-funds/',views.withdrawal_view, name="withdraw"),
    path('history/',views.history_view, name="history"),
    path('renew-subscription/',views.renew_investment_view, name="renew_sub"),
    path('credit-user/',views.user_daily_income, name="credit-user"),
    
 
]
