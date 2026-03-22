from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('forgot/', views.forgot_password, name='forgot'),
    path('verify-otp/', views.verify_otp),
]
