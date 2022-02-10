from django.urls import path


from . import views




urlpatterns = [
    path('',views.home_view, name="homepage"),
    path('about/',views.about_view, name="aboutpage"),
    path('contact/',views.contact_view, name="contactpage"),
    path('verify-token/',views.verify_code_view, name="verifycodepage"),
     path('token-dealers/',views.vendors_view, name="vendorspage"),
]
