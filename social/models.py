from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
	class Meta:
		ordering = ["id"]
		verbose_name_plural = "Quản lý tài khoản"
	AbstractUser._meta.get_field('email').blank = False
	AbstractUser._meta.get_field('email').null = False
	AbstractUser._meta.get_field('username').blank = False
	AbstractUser._meta.get_field('username').null = False
	AbstractUser._meta.get_field('password').blank = False
	AbstractUser._meta.get_field('password').null = False

class Data_zip_exel(models.Model):
    zip_file = models.FileField(upload_to='',null=True, blank=True)
    image_file = models.FileField(upload_to='',null=True, blank=True)