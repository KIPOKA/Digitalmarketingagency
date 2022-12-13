from django.urls import path
from digitalapp import views

urlpatterns = [
    path('', views.home, name='home')
]
