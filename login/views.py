from django.shortcuts import render
from django.contrib.auth import login,authenticate
from .forms import SignUpForm, PostForm
from django.shortcuts import render,redirect
from django.views.generic import ListView, CreateView
from . import models
from django.urls import reverse_lazy

    
def home_view(request):
    object = models.Post.objects.all()
    return render(request,'home.html',{'object':object})


def upload_view(request):
    if request.method=='POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home_view')
        else:
            return render(request,'upload.html',{'form':form})
    else:
        form = PostForm()
    return render(request,'upload.html',{'form':form})

def login_view(request):
    if request.method=='POST':
        username = request.POST['user']
        password = request.POST['user_pass']
        user = authenticate(username = username,password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                return redirect('home_view')
            else:
                return render(request,'login.html',{'err': 'session timeout'})
        else:
            return render(request,'login.html',{'err':'wrong credentials'})
    return render(request,'login.html',{'err':''})

def signup_view(request):
    if request.method=='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username,password=password)
            login(request,user)
            return redirect('home_view')
        else:
            return render(request,'signup.html',{'form':form})
    else:
        form = SignUpForm()
    return render(request,'signup.html',{'form':form})
