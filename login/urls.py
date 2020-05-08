from django.contrib import admin
from . import views
from django.urls import path, include
from django.conf.urls import url

urlpatterns=[
    path('signup/',views.signup_view,name='signup_view'),
    path('',views.home_view,name='home_view'),
    path('login/',views.login_view, name='login_view'),
    path('upload/',views.upload_view, name='upload_view'),
    path('logout/',views.logout_view, name='logout_view'),
    path('search/',views.search_view,name='search_view'),
    path('approve/',views.approve_view,name='approve_view'),
    path('approved/',views.approve_file_view,name='approve_file_view'),
    url(r'^ajax_calls/search/', views.autocompleteModel),
    # path('approve/<id>/delete', views.delete_view, name='delete_view'),
    path('sample/',views.sample_view,name='sample_view'),
    path("logout", views.logout_request, name="logout"),
    path('category/',views.list_of_categories,name='list_of_categories'),
    path('category/<category_slug>',views.list_of_post_by_category,name='list_of_post_by_category'),
    path('category/<category_slug>/<id>/',views.object_view,name='object_view'),
    path('category/<category_slug>/<id>/comment/',views.add_comment,name = 'add_comment'),
    url(r'^rate_vector/(?P<vector_id>[0-9]+)$', views.rate_vector, name="rate_vector"),
    
]