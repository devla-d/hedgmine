from django.urls import path


from django.contrib.auth import  views as auth_view

from . import views




urlpatterns = [
    path('',views.account_view, name="accountpage"),
    path('get-started/',views.register_view, name="registerpage"),
    path('sign-in/',views.login_view, name="loginpage"),
    path('sign-out/',views.logout_view, name="logout"),



    path('password-reset/', auth_view.PasswordResetView.as_view(template_name='auth/password-reset.html'), name='password-reset'),
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='auth/password-reset-done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>', auth_view.PasswordResetConfirmView.as_view(template_name='auth/password-reset-confirm.html'), name='password_reset_confirm'),
    path('password-reset/complete/', auth_view.PasswordResetCompleteView.as_view(template_name='auth/password-reset-complete.html'), name='password_reset_complete'),
 
]
