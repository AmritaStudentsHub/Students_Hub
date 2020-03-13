from django.contrib import admin
from . import views
from django.urls import path, include

urlpatterns=[
    path('signup/',views.signup_view,name='signup_view'),
    path('',views.home_view,name='home_view'),
    path('login/',views.login_view, name='login_view'),
    path('upload/',views.upload_view, name='upload_view'),
    path('logout/',views.logout_view, name='logout_view'),
    path('sample/',views.sample_view, name='sample_view'),
]