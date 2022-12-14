from django.urls import path
from digitalapp import views

urlpatterns = [
    path('', views.home, name='home'),
    path('purchase', views.purchase, name='purchase'),
    path('purchase', views.checkout, name='checkout'),
]
