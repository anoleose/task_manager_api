#coding: 'utf-8'
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy, reverse
from django.template import loader
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from accounts.models import UserProfile, Task
from django.views.generic import*
from django.contrib.auth import update_session_auth_hash, get_user_model, login, authenticate #permet de garder l'authentification de l'utilisateur
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from .forms import (
	RegistrationForm, 
	EditProfileForm, 
	UserProfileForm, 
	PasswordFormChange, 
	AddTaskForm,
	EditTaskForm,
	DeleteTaskForm,
	)
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
import smtplib 
import datetime
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from .serializers import TaskSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
import requests


def Signup(request):
	if request.method == "POST":
		form = RegistrationForm(request.POST)	
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Account Created successfully For {username}!')
			return redirect('accounts_app:login')
			

	else:
		form = RegistrationForm()
	context = {
			'form':(form),
		}

	if request.user.is_authenticated:
		return redirect('accounts_app:profile')
	else:
		form = RegistrationForm()

	template = loader.get_template('accounts/signup_form.html')
	return HttpResponse(template.render (context, request))



@login_required
def profile(request):
	task = Task.objects.private_tasks(user=request.user)
	instance = Task.objects.private_tasks(user=request.user)
	try:
		query = request.GET.get("search")
	except:
		query = None
	if query:
		task = Task.objects.filter(Q(status__icontains=query) | Q(deadline__icontains=query)).distinct()
		context = {
		'user':(request.user),
		'task':task,
		'instance': instance,
		'query':query
		}
		return render(request, 'accounts/list_task.html', context)
	else:
		context = {
		'user':(request.user),
		'task':task,
		'instance':instance,
		
		}
		return render(request, 'accounts/profile.html', context)
	template = loader.get_template('accounts/profile.html')
	return HttpResponse(template.render (context, request))




@login_required
def edit_profile(request):
	task = Task.objects.all()
	if request.method == 'POST':
		e_form  = EditProfileForm(request.POST, instance=request.user)
		ed_form = UserProfileForm(request.POST, instance=request.user)
		if e_form.is_valid() and ed_form.is_valid():
			e_form.save()
			ed_form.save()
			username = e_form.cleaned_data.get('username')
			messages.success(request, f'Your Account Have Been Updated {username}!')
			return redirect('accounts_app:profile')
	else:
		e_form  = EditProfileForm(instance=request.user)
		ed_form = UserProfileForm(instance=request.user)
		

	context = {
		'e_form':(e_form),
		'ed_form':(ed_form),
		'task':task
			
	}
	template = loader.get_template('accounts/edit_profile.html')
	return HttpResponse(template.render (context, request))



@login_required
def change_password(request):
	task = Task.objects.all()
	if request.method == 'POST':
		form = PasswordFormChange(data=request.POST, user=request.user)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			return redirect('accounts_app:profile')
		else:
			return redirect('accounts_app:change_password')

	else:
		form = PasswordFormChange(user=request.user)
		context = {
			'form':(form),
			'task':task
		}
		template = loader.get_template('accounts/change_password.html')
		return HttpResponse(template.render (context, request))

@login_required
def list_task(request):
	task  = Task.objects.private_tasks(user=request.user)
	hist  = Task.history.private_history(user=request.user)
	query = request.GET.get("search")
	q = Task.objects.private_tasks(status__icontains='completed', user=request.user)
	p = Task.objects.private_tasks(status__icontains='Planned', user=request.user)	
	n = Task.objects.private_tasks(status__icontains='News',  user=request.user)	 
	i = Task.objects.private_tasks(status__icontains='In process',  user=request.user)
	if query:
		task = Task.objects.filter(Q(status__icontains=query) | Q(deadline__icontains=query)).distinct()


	context = {
		'task':task,
		'query':query,
		'q':q,
		'p':p,
		'n':n,
		'i':i,
		'hist':hist
	}

	template = loader.get_template('accounts/list_task.html')
	return HttpResponse(template.render(context, request))

@login_required
def detail_task(request,title, id):
	task     = get_object_or_404(Task, title=title, id=id)
	instance = Task.objects.all()

	context = {
		'task' : task,
		'instance': instance
	}

	template = loader.get_template('accounts/detail_task.html')
	return HttpResponse(template.render(context, request))


@login_required
def add_task(request):
	task = Task.objects.all()
	if request.method == 'POST':
		form = AddTaskForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, f'Account Created successfully For')
			return redirect('accounts_app:tasks')
	else:
		form = AddTaskForm()

	context = {
		'form':form,
		'task':task
	}

	template = loader.get_template('accounts/add_task_form.html')
	return HttpResponse(template.render(context, request))

@login_required
def update_task(request, title, id):
	task     = Task.objects.all()
	instance = get_object_or_404(Task, title=title, id=id)
	if request.method == 'POST':
		form = EditTaskForm(request.POST, instance=instance)
		if form.is_valid():
			form.save()
			instance.history.most_recent()
			messages.success(request, f'Task Updated')
			return redirect('accounts_app:profile')
	else:
		form = EditTaskForm(instance=instance)

	context = {
		'form':form,
		'task':task,
	}

	template = loader.get_template('accounts/edit_task_form.html')
	return HttpResponse(template.render(context, request))

@login_required
def delete_task(request, title, id):
	task     = Task.objects.all()
	instance = get_object_or_404(Task, title=title, id=id)
	if request.method == 'POST':
		form = DeleteTaskForm(request.POST, instance=instance)
		if form.is_valid():
			instance.delete()
			messages.success(request, f'Task has been deleted successfully')
			return redirect('accounts_app:tasks')

	else:
		form = DeleteTaskForm(instance=instance)

	context = {
		'form':form,
		'task':task,
		'instance':instance
	}


	template = loader.get_template('accounts/task_confirm_delete.html')
	return HttpResponse(template.render(context, request))


@api_view(['GET'])
def api_views(request):
	api_urls = {
		'List': '/task-list/', 
		'Detai-View':'/task-detail/<str:pk>/', 
		'Create': '/task-create/<str:pk>/', 
		'Update': '/task-update/<str:pk>/', 
		'Delete': '/task-delete/<str:pk>/', 
		}
	return JsonResponse(api_urls)

@login_required
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def task_list(request):
	tasks      = Task.objects.private_tasks(user=request.user)
	serializer = TaskSerializer(tasks, many=True)
	context    = {
		'serializer':serializer
	}
	return JsonResponse(serializer.data, safe=False)


@login_required
@api_view(['GET'])
def task_detail(request, title, id):
	tasks      = Task.objects.get(title=title, id=id)
	serializer = TaskSerializer(tasks, many=False)
	return Response(serializer.data)

@login_required
@api_view(['POST'])
def task_create(request):
	serializer = TaskSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()
	return Response(serializer.data)

@login_required
@api_view(['POST'])
def task_update(request, title, id):
	tasks      = Task.objects.get(title=title, id=id)
	serializer = TaskSerializer(instance=tasks, data=request.data)
	if serializer.is_valid():
		serializer.save()
	return Response(serializer.data)

@login_required
@api_view(['DELETE'])
def task_delete(request, title, id):
	tasks = Task.objects.get(title=title, id=id)
	tasks.delete()
	return Response('Item has been deleted successfully')

@login_required
def api_service(request):
	context = {

	}
	template = loader.get_template('accounts/api_service.html')
	return HttpResponse(template.render(context, request))

@login_required
def api_generate_token(request, key):
	token = Token.objects.get(user=request.user)
	print(token)
	context = {
	'token':token.key,
	}
	template = loader.get_template('accounts/api_generate_token.html')
	return HttpResponse(template.render(context, request))








