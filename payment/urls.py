from django.contrib import admin
from django.urls import path, include
from payment import views

app_name = 'payment'
urlpatterns = [
    path('process/', views.payment_process, name='process'),
    path('done/', views.payment_done, name='done'),
    path('canceled/', views.payment_canceled, name='canceled'),

]
