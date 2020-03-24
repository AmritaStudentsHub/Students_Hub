from django.shortcuts import render
from django.contrib.auth import login,authenticate,logout
from .forms import SignUpForm, PostForm
from django.shortcuts import render,redirect
from django.views.generic import ListView, CreateView
from . import models
from django.urls import reverse_lazy
import json
from django.http import HttpResponse
    
def home_view(request):
    object = models.Post.objects.all()
    return render(request,'home.html',{'object':object})

def sample_view(request):
    return render(request,'sample.html')

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

def logout_view(request):
    logout(request)
    return redirect(home_view)

def autocompleteModel(request):
    if request.is_ajax():
        q = request.GET.get('term', '').capitalize()
        search_qs = models.Post.objects.filter(title__startswith=q)
        results = []
        print (q)
        for r in search_qs:
            results.append(r.title)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
