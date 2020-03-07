from django.contrib import admin
from . import views
from django.urls import path, include

urlpatterns=[
    path('signup',views.signup_view,name='signup_view'),
    path('',views.home_view,name='home_view'),
    path('login/',views.login_view, name='login_view'),
]