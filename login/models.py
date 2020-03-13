from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100,blank=True)
    last_name = models.CharField(max_length=100,blank=True)
    email = models.EmailField(max_length=150)

    def __str__(self):
        return self.user.username

@receiver(post_save,sender=User)
def update_profile_signal(sender, instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Post(models.Model):
    title = models.TextField()
    pdf = models.FileField(upload_to='pdfs/',blank = True,null=True,default='null')
    link = models.CharField(max_length=100,blank=True)
    rating = models.FloatField(default=0,max_length=5)

    def __str__(self):
        return self.title

