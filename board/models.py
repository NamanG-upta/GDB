from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager
from django.conf import settings


class NewUser(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	contact = models.CharField(max_length=20, blank=True)
	institute_name = models.CharField(max_length=200, blank=True)

	def __str__(self):
		return self.user.first_name

class helptext(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	text = models.TextField(max_length=500,blank=True, null=True)

	def __str__(self):
		return self.text


class Task(models.Model):
	title = models.CharField(max_length=200)
	desc = models.CharField(max_length=500)
	complete = models.BooleanField(default=False)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	board_id = models.CharField(max_length=20, blank=True, null=True)
	ip_address = models.CharField(max_length=200,blank=True, null=True) 
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title