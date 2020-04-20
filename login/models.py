from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.core.validators import MaxValueValidator,MinValueValidator

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
    course = models.TextField(blank=False,null=False)
    title = models.TextField()
    pdf = models.FileField(upload_to='pdfs/',blank = True,null=True)
    link = models.CharField(max_length=100,blank=True)
    access = models.BooleanField(default=False)
    rating = models.FloatField(default=0.0)

    def update_rating(self):
        r = self.ratings.all().aggregate(rating=models.Avg("rating"))
        self.rating = round(r["rating"], 2) if r["rating"] is not None else 0
        self.save()

    def __str__(self):
        return self.title

class Review(models.Model):
    user = models.ForeignKey(Profile,on_delete=models.CASCADE)
    reviewed_file = models.ForeignKey(Post,related_name="ratings",on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, validators=[MinValueValidator(0),MaxValueValidator(5)])

    @staticmethod
    def update_avg_rating(sender,instance,**kwargs):
        instance.reviewed_file.update_rating()

post_delete.connect(Review.update_avg_rating,sender=Review)
post_save.connect(Review.update_avg_rating,sender=Review)