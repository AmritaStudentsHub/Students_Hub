from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post,Comment,Category

class SignUpForm(UserCreationForm):
    # first_name = forms.CharField(max_length=100,help_text='First Name')
    # last_name = forms.CharField(max_length=100,help_text='Last Name')
    # email = forms.EmailField(max_length=150,help_text='Email')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                'class': 'form-control',
                                                                }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name',
                                                                'class': 'form-control',
                                                                }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name',
                                                                'class': 'form-control',
                                                                }))
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email',
                                                                'class': 'form-control',
                                                                }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password',
                                                                'class': 'form-control',
                                                                }))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                                'class': 'form-control',
                                                                }))
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1','password2',)
    def __init__(self,*args,**kwargs):
        super(SignUpForm,self).__init__(*args,**kwargs)
        


class PostForm(forms.ModelForm):

    # category = forms.CharField(widget=forms.TextInput(attrs={'class':'contact-input,'}))
    title =  forms.CharField(widget=forms.TextInput(attrs={'class':'contact-input,'}))

    class Meta:
        model = Post
        fields=['category','title','pdf','link']

# class CategoryForm(forms.ModelForm):
#     class Meta:
#         model = Category
#         fields = ['name']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields=['user','body']