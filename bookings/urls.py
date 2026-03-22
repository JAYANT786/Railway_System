from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:train_id>/', views.book_ticket, name='book_ticket'),
    path('my-bookings/', views.booking_history, name='booking_history'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('payment/<int:booking_id>/', views.payment_page, name='payment_page'),
    path('payment-success/<int:booking_id>/', views.payment_success, name='payment_success'),
]