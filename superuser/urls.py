from django.urls import path


from . import views




urlpatterns = [
    path('',views.dashboard_view, name="adminpage"),
    path('users/',views.users_view, name="userspage"),
    path('user/<int:pk>/',views.user_detail_view, name="user_detail"),
    path('withdrawals/',views.withdrawals_view, name="withdrawals"),
    path('withdrawal/<int:pk>/',views.withdrawal_detail_view, name="withdrawal_detail"),

    path('tokens/',views.tokens_view, name="tokens"),
    path('create-token/',views.create_tokens_view, name="create-token"),


]