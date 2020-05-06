from django.contrib.auth import login,authenticate,logout
from .forms import SignUpForm, PostForm, CommentForm
from django.shortcuts import render,redirect,get_object_or_404,HttpResponseRedirect
from django.views.generic import ListView, CreateView
from django.views.decorators.csrf import csrf_exempt
from . import models
from django.urls import reverse_lazy
import json
from django.http import HttpResponse,JsonResponse
from django.views.decorators.http import require_POST
    
def home_view(request):
    object = models.Post.objects.all()
    categories = models.Category.objects.all()
    print (categories)
    approvals = models.Post.objects.filter(access=False).count()
    return render(request,'index.html',{'object':object,'approvals':approvals,'categories':categories})
    # if request.method == 'POST':
    #     name = request.POST['txtSearch']
    #     print (name)
    #     if name is not None:
    #         print('searching')
    #         object = models.Post.objects.filter(title__startswith=name)
    #         return render(request,'home.html',{'object':object})
    #     print ('name is none')
    #     return render(request,'home.html',{'object':object})
    # else:
    #     return render(request,'home.html',{'object':object})

def approve_view(request):
    object = models.Post.objects.all()
    approvals = models.Post.objects.filter(access=False).count()
    print (object)
    if request.user.is_staff:
        object = models.Post.objects.filter(access=False)
        print(object)
        return render(request,'contact.html',{'object':object,'approvals':approvals})
    else:
        return HttpResponse('You don\'t have access to this page')

def logout_request(request):
    logout(request)
    return redirect("/")

def add_comment(request,category_slug,id):
    post = get_object_or_404(models.Post,id=id)
    if request.method=='POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            print('saved')
            return redirect('object_view',category_slug=post.category,id=post.id)
    else:
        intial = {'user':request.user.username}
        form=CommentForm(initial=intial)
    return render(request,'add_comment.html',{'form':form})
@csrf_exempt
def search_view(request):
    print (request)
    if request.method == 'GET':
        name = request.GET['txtSearch']
        object = models.Post.objects.filter(title__startswith=name,access=True)
        return render(request,'search.html',{'object':object,'name':name})

def upload_view(request):
    if request.method=='POST':
        # print (request.Post,request.values)
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            print (form)
            return redirect('home_view')
        else:
            return render(request,'about.html',{'form':form})
    else:
        form = PostForm()
    return render(request,'about.html',{'form':form})

def object_view(request,category_slug,id):
    post = get_object_or_404(models.Post,id=id)
    return render(request,'object_view.html',{'post':post,'category_slug':category_slug})

def approve_file_view(request):
    object = models.Post.objects.all()
    print ('it is working')
    # set the status if request method is post
    if request.method == "POST":
        order_id = request.POST.get("id")
        print (order_id)
        # get order instance by id and change the status
        order = models.Post.objects.get(pk=order_id)
        order.access = True
        order.save()
    # since the render data is the same, you can just call it once.
    return redirect('http://localhost:8000/approve/')
    # return render(request, 'approve_page.html', {'object':object})

def delete_view(request,id):
    if request.user.is_staff:
        obj = get_object_or_404(models.Post, id = id) 
    
        if request.method =="POST": 
            # delete object 
            obj.delete() 
            # after deleting redirect to  
            # home page 
            return HttpResponseRedirect("/") 
    
        return render(request, "delete_view.html")
    else:
        return redirect('/')
    # print ('delete is working')
    # return approve_view(request)

def sample_view(request):
    return render(request,'samplehome.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
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
    if request.user.is_authenticated:
        return redirect('/')
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
        search_qs = models.Post.objects.filter(title__startswith=q,access=True)
        results = []
        print (q)
        for r in search_qs:
            results.append(r.title)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def autocompleteModel1(request):
    if request.is_ajax():
        q = request.GET.get('term', '').capitalize()
        search_qs = models.Post.objects.filter(course__startswith=q)
        results = []
        print (q)
        for r in search_qs:
            results.append(r.course)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

@require_POST
def rate_vector(request, vector_id):
    # if not request.user.is_authenticated():
    #     return HttpResponseForbidden()

    rating = request.POST['rating']

    vector = get_object_or_404(models.Post, id=vector_id)

    # try:
    #     vector_rating = models.Review.objects.get(rating=vector, user=request.user)
    #     created = False
    # except ObjectDoesNotExist:
    #     vector_rating = models.Review(rating=vector, user=request.user)
    #     created = True
    vector_rating = models.Review(reviewed_file=vector, user=request.user)
    #vector_rating, created = VectorRating.objects.get_or_create(vector=vector, user=request.user)
    vector_rating.rating = rating
    vector_rating.save()

    data = {
        "rating": vector_rating.reviewed_file.rating
    }
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def list_of_post_by_category(request,category_slug):
    categories = models.Category.objects.all()
    post = models.Post.objects.filter(access=True)

    if category_slug:
        category = get_object_or_404(models.Category,slug=category_slug)
        post = post.filter(category=category)
    context = {'object':post,'category':category}
    return render(request,'category.html',context)

def list_of_categories(request):
    post = models.Post.objects.filter(access=True)
    categories = models.Category.objects.all()
    return render(request,'services.html',{'categories':categories,'object':post})
