from django.contrib.auth.models import Group, Permission, User ,AbstractUser
from django.db import models

class Login(AbstractUser):  
    userType=models.CharField(max_length=50)
    viewpassword=models.CharField(max_length=50,null=True)
    def __str__(self):
        return self.username
    
    

class user_reg(models.Model):
    user=models.OneToOneField(Login,on_delete=models.CASCADE,null=True)
    user_full_name=models.CharField(max_length=100,null=True)
    img=models.ImageField(upload_to='profile-image/',null=True)
    user_email=models.EmailField(null=True)
    user_password=models.TextField(null=True)
    date=models.DateField(null=True)
    

class contact(models.Model):
    fullname=models.CharField(max_length=100,null=True)
    mail=models.EmailField(max_length=100,null=True)
    subject=models.CharField(max_length=100,null=True)
    message=models.TextField(max_length=400,null=True)
    date=models.DateField(null=True)
    
class Addproduct(models.Model):
    id=models.IntegerField(primary_key=True)
    movie_title=models.TextField(max_length=100,null=True)
    movie_desc=models.TextField(max_length=300,null=True)
    movie_cover=models.ImageField(null=True)
    movie_video=models.FileField(null=True)
    movie_trailer=models.FileField(null=True)
    movie_age=models.IntegerField(null=True)
    movie_year=models.IntegerField(null=True)
    movie_time=models.TextField(max_length=100,null=True)
    movie_country=models.TextField(max_length=100,null=True)
    movie_genre=models.TextField(max_length=100,null=True)
    movie_director=models.TextField(max_length=100,null=True)
    movie_cast=models.TextField(max_length=300,null=True)
    date=models.DateField(null=True)
    priority=models.IntegerField(default=5)

class comments(models.Model):
    user_id=models.ForeignKey(user_reg,on_delete=models.CASCADE,null=True) 
    comment=models.TextField(max_length=100,null=True)
    cdate=models.DateField(null=True)
    product_id=models.ForeignKey(Addproduct,on_delete=models.CASCADE,null=True)

class rating(models.Model):
    user_id=models.ForeignKey(user_reg,on_delete=models.CASCADE,null=True)  
    product_id=models.ForeignKey(Addproduct,on_delete=models.CASCADE,null=True)
    reviewtitle=models.TextField(max_length=300,null=True)
    review=models.TextField(max_length=300,null=True)
    date=models.DateField(null=True)
    star_rating = models.PositiveIntegerField(default=0,null=True)
    
class watchlater(models.Model):
    product_id=models.ForeignKey(Addproduct,on_delete=models.CASCADE,null=True)
    user_id=models.ForeignKey(user_reg,on_delete=models.CASCADE,null=True)
