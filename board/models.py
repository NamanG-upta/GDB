from django.db import models
from django.contrib.auth.models import User


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