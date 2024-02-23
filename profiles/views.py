import re
from urllib import request
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . forms import UserRegistrationForm, UserUpdateForm, UserProfileUpdateForm, ChangePasswordForm
from django.contrib.auth.models import User
from videos.models import VidStream
from .models import Profile
from photos.models import Photo


def register(request):
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('login')
	else: 
		form=UserRegistrationForm()
	return render(request, 'profiles/register.html', {'form': form})


@login_required
def profile(request):
	if request.method == 'POST':
		userform=UserUpdateForm(request.POST, instance=request.user)
		profileform= UserProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		if userform.is_valid() and profileform.is_valid():
			userform.save()
			profileform.save()
			return redirect('profile')
	else: 
		userform=UserUpdateForm(instance=request.user)
		profileform=UserProfileUpdateForm(instance=request.user.profile)
		#change_password_form=ChangePasswordForm(instance=request.user)
	
	videos =VidStream.objects.filter(uploader=request.user)
	photos =Photo.objects.filter(uploader=request.user)
		

	context ={
		'userform':userform,
		'profileform': profileform,
		'videos':videos,
		'photos':photos
	}
	return render(request, 'profiles/profile.html', context)



def password(request):
	if request.method== 'POST':
		password_form= ChangePasswordForm(request.POST, instance=request.user.profile)
		if password_form.is_valid():
			password_form.save
		return render(request,'profiles/password_reset.html', {'password_form':password_form})

	else: password_form=ChangePasswordForm(instance=request.user)

	context={'password_form':password_form}
	
	return render(request,'profiles/password_reset.html', context)




