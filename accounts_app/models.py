#coding:utf-8
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.urls import reverse
from simple_history.models import HistoricalRecords
from django.dispatch import receiver
from rest_framework.authtoken.models import Token




class TaskManager(models.Manager):
	def private_tasks(self, *arg, **kwargs):
		user= kwargs.pop('user')
		return super(TaskManager, self).filter(public=False, user=user)
	
class Task(models.Model):

	STATUS_CHOICES = (
		('News', 'News'),
		('Planned', 'Planned'),
		('In process', 'In process'),
		('Completed', 'Completed'),

	)

	user       = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
	title      = models.CharField(max_length=200)
	content    = models.TextField()
	deadline   = models.DateField(auto_now=False, null=True, blank=True)
	status     = models.CharField( choices=STATUS_CHOICES, max_length=100, default='In process')
	public     = models.BooleanField(default=False)
	created_to = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	update_to  = models.DateTimeField(auto_now=True, auto_now_add=False)
	history    = HistoricalRecords()

	objects    = TaskManager()

	
	def __str__(self):
		return self.title

	class Meta:
		verbose_name_plural = "Tasks"
		ordering = ['-created_to']

	
	def get_absolute_url(self):
		return reverse("accounts_app:details", kwargs={'title': self.title, 'id': self.id})

	def get_update_url(self):
		return reverse("accounts_app:update-task", kwargs={'title': self.title, 'id': self.id})

	def get_delete_url(self):
		return reverse("accounts_app:delete-task", kwargs={'title': self.title, 'id': self.id})




class UserProfile(models.Model):
	MALE = 'M'
	FEMALE = 'F'
	GENDER_CHOICE = [
		(MALE, 'M'),
		(FEMALE,'F'),
	]

	user        = models.OneToOneField(User, on_delete=models.CASCADE)
	description = models.CharField(max_length=100, default='')
	birthday    = models.DateField(auto_now=False, null=True, blank=True)
	gender      = models.CharField(
        max_length=2,
        choices=GENDER_CHOICE,
        default=MALE,
    )
	photo       = models.ImageField(upload_to='accounts_image_userprofile/', blank=True)
  
    
	def __str__(self):
		return self.user.username




def create_profile(sender, **kwargs):
	if kwargs['created']:
		userprofile = UserProfile.objects.create(user=kwargs['instance'])

	post_save.connect(create_profile, sender=User)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
       
