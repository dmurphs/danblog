from django import forms
from django.contrib.auth.models import User
from .models import BlogUser

class UserForm(forms.ModelForm):

	class Meta:
		model = User
		fields = ('username', 'password', 'email')

class BlogUserForm(forms.ModelForm):
	class Meta:
		model = BlogUser
		fields = ('first_name', 'last_name', 'summary', 'website', 'image')