from django.shortcuts import render
from .forms import UserForm, BlogUserForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponseRedirect
from vanilla import UpdateView
from .models import User, BlogUser
from django.contrib.auth.decorators import login_required

def login(request):
	if request.method == 'POST':
		
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username=username, password=password)

		if user:
			if user.is_active:
				auth_login(request, user)
				return HttpResponseRedirect('/')

			else:
				return HttpResponse("Your account is disabled.")

		else:
			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login details supplied.")

	else:
		return render(request, 'login.html', {})

def logout(request):
	auth_logout(request)
	return HttpResponseRedirect('/')

def register(request):

	registered = False

	if request.method == 'POST':
		
		user_form = UserForm(data=request.POST)
		blog_user_form = BlogUserForm(data=request.POST)

		if user_form.is_valid() and blog_user_form.is_valid():

			user = user_form.save()

			user.set_password(user.password)
			user.save()

			blog_user = blog_user_form.save(commit=False)
			blog_user.user = user

			if 'image' in request.FILES:
				blog_user.image = request.FILES['image']

			blog_user.save()

			registered = True

	else:
		user_form = UserForm()
		blog_user_form = BlogUserForm()

	return render(request,
            'register.html',
            {'user_form': user_form, 'blog_user_form': blog_user_form, 'registered': registered} )

def user_detail(request, user_id):
	base_user = User.objects.get(id = user_id)
	blog_user = BlogUser.objects.get(user = base_user)

	return render(request, 'profile.html', {'base_user': base_user, 'blog_user': blog_user})

@login_required
def edit_profile(request):
	base_user = request.user
	blog_user = BlogUser.objects.get(user=base_user)

	if request.method == 'POST':
		form = BlogUserForm(data=request.POST, instance=blog_user)
		if form.is_valid():
			updated_user = form.save(commit=False)

			if 'image' in request.FILES:
				updated_user.image = request.FILES['image']

			updated_user.save()

			return HttpResponseRedirect('/')
	else:
		form = BlogUserForm(instance=blog_user)

	return render(request, 'edit_user.html', {'form': form})