from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100,help_text='First Name')
    last_name = forms.CharField(max_length=100,help_text='Last Name')
    email = forms.EmailField(max_length=150,help_text='Email')

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1','password2',)

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields=['title','pdf','link']