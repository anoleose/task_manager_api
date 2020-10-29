#coding:'utf-8'
from django.urls import path, include
#from accounts.views import activate
from . import views
from accounts.views import *
from django.urls import reverse_lazy

from django.contrib.auth.views import (
	LoginView,
	LogoutView, 
	PasswordResetView, 
	PasswordResetDoneView, 
	PasswordResetConfirmView,
	PasswordResetCompleteView
	)

from .forms import UserLoginForm
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required 
from rest_framework.authtoken.views import obtain_auth_token 


app_name = 'accounts_app'




urlpatterns = [
	path('', LoginView.as_view(
		template_name='accounts/login.html', redirect_authenticated_user=True,
		authentication_form = UserLoginForm), name="login"),
	path('logout/', login_required(LogoutView.as_view(template_name='accounts/logout.html',)), name="logout"),
	path('signup/', views.Signup, name='signup'),
	path('profile/', views.profile, name="profile"),
	path('profile/update/', views.edit_profile, name="edit_profile"),
	path('change-password/', views.change_password, name="change_password"),
	path('password-reset/', PasswordResetView.as_view(template_name='accounts/password_reset.html',  success_url = reverse_lazy('accounts:password_reset_done'), email_template_name= 'accounts/password_reset_email.html'), name="password-reset"),
	path('password-reset/done/', PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
	path('password-reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html',  success_url = reverse_lazy('accounts:password_reset_complete')), name="password_reset_confirm"),
	path('password-reset/complete/', PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name="password_reset_complete"),
	path('tasks/', views.list_task, name='tasks'),
	path('details/<title>/<int:id>/', views.detail_task, name='details'),
	path('add-task/', views.add_task, name='add_task'),
	path('details/<title>/<int:id>/update-task/', views.update_task, name='update-task'),
	path('details/<title>/<int:id>/delete-task/', views.delete_task, name='delete-task'),
	path('api-auth/', views.api_views, name="api_auth"),
	path('api-task-list/', views.task_list, name="api-task-list"),
	path('api-task-detail/<title>/<int:id>/', views.task_detail, name='api-task-detail'),
	path('api-task-create/', views.task_create, name="api-task-create"),
	path('api-task-update/<title>/<int:id>/', views.task_update, name='api-task-update'),
	path('api-task-delete/<title>/<int:id>/', views.task_delete, name='api-task-delete'),
	path('api-service/', views.api_service, name='api-service'),
	path('api-generate-token/<key>/', views.api_generate_token, name='api-generate-token'),


	];