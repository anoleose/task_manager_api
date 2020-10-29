#coding:'utf-8'
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import( 
	AuthenticationForm, 
	UserCreationForm, 
	UserChangeForm, 
	SetPasswordForm, 
	PasswordChangeForm
	)
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from accounts.models import UserProfile, Task
from datetime import datetime

def EmailValide( email ):
	
	validate_email = EmailValidator()
	
	try:
		validate_email(email)
	except:
		return ValidationError("not valid email")
	return email 


class UserLoginForm(AuthenticationForm):
	def __init__(self, *args, **kwargs):
		super(UserLoginForm, self).__init__(*args, **kwargs)

	username = username = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Email или Имя"}))
	password = forms.CharField(label='', required=True, widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Пароль"}))




class RegistrationForm(UserCreationForm):
	username  = forms.CharField(label="", widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Имя"}))
	email     = forms.EmailField(validators=[EmailValidator], label="", required=True, widget=forms.EmailInput(attrs={"class":"form-control","placeholder":"Email"}))
	password1 = forms.CharField(label="", required=True, widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Пароль"}))
	password2 = forms.CharField(label="", required=True, widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Подтвердите пароль"}))
	class Meta:
		model  = User
		fields = (
			'username',
			'email',
			'password1',
			'password2',
		)
	
	

	def save(self, commit=True):
		user          = super(RegistrationForm, self).save(commit=False)
		user.username = self.cleaned_data['username']
		user.email    = self.cleaned_data['email']

		if commit:
			user.save()

		return user 


class EditProfileForm(forms.ModelForm):
	username   = forms.CharField(label="Имя", widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Имя"}))
	first_name =  forms.CharField(label="Фамилия", widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Фамилия"}))
	last_name  =  forms.CharField(label="Очество", widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Очество"}))
	email      = forms.EmailField(label="Email", required=True, widget=forms.EmailInput(attrs={"class":"form-control","placeholder":"Email"}))


	class Meta:
		model  = User 
		fields = (

			'username',
			'first_name',
			'last_name',
			'email',

		)


class UserProfileForm(forms.ModelForm):

	class Meta:
		model  = UserProfile
		fields = (
			
			'birthday',
			'description',
			'gender',
			'photo',
			)


class PasswordFormChange(PasswordChangeForm):
	
	old_password  = forms.CharField(label="", required=True, widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Пароль"}))
	new_password1 = forms.CharField(label="", required=True, widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Новый парполь"}))
	new_password2 = forms.CharField(label="", required=True, widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Подтвердите пароль"}))
	class Meta:
		model  = User
		fields = (
			'old_password',
			'password1',
			'password2',
		)
	

class AddTaskForm(forms.ModelForm):
#creation = forms.DateTimeField(label="created",initial=datetime.now().strftime("%H:%M"), required=True)
#deadline = forms.DateTimeField(initial=datetime.now().strftime("%d-%m-%Y"), required=True)

	class Meta:
		model = Task
		fields = (
			'title',
			'content',
			'status',
			'deadline',
		)


class EditTaskForm(forms.ModelForm):
	class Meta:
		model  = Task
		fields = (
			'title',
			'content',
			'status',
			'deadline',
			)

class DeleteTaskForm(forms.ModelForm):
	class Meta:
		model  = Task
		fields = []
