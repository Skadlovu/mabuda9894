from django.shortcuts import render, redirect, get_object_or_404
from . models import Photo
from . forms import PhotoUploadForm
from django.views.generic import DetailView, DeleteView, UpdateView, ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from videos.models import Comment
from videos.forms import CommentForm



def get_photo(request, id):
	template='photos/photo.html'
	photo=Photo.objects.get(id=id)
	comments=Comment.objects.filter(photo=id)

	form=CommentForm()
	if request.method=='POST':
		form=(request.POST)
		if form.is_valid:
			comment=form.save(commit=False)
			comment.user=request.user
			comment.save()
			return redirect('photo', id=id)
	
	context={'photo': photo, 'comments':comments, 'form':form}

	return render(request,template,context)


	


@login_required
def create_photo(request):
	template='photos/photo_create.html'
	if request.method=='POST':
		form=PhotoUploadForm(request.POST, request.FILES)
		if form.is_valid:
			photo_instance=form.save(commit=False)
			photo_instance.uploader=request.user
			photo_instance.save()
			return redirect('photos')
	else:
		form=PhotoUploadForm()
		
	return render(request,template,{'form': form} )



def all_photos(request):
	template='photos/photos.html'
	photos=Photo.objects.all().order_by('-upload_date')
	return render(request, template,{'photos':photos})



def search(request):
	if request.method== 'POST':
		query=request.POST.get('title', None)
		if query:
			results= Photo.objects.filter(title_contains= query)
			return render(request, 'photos/search.html'), {'content':results}
	return render(request('photos/search.html'))

