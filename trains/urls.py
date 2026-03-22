from django.urls import path
from . import views

urlpatterns = [
    path('', views.train_list, name='train_list'),
]