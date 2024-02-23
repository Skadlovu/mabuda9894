from django.db.models.query import QuerySet
from .thumb_generator import thumb_generator 
from django.shortcuts import render, redirect,get_object_or_404
from . models import VidStream, Category, Comment
from . forms import VideoUploadForm,CommentForm,LikeForm
from django.contrib.auth.models import User
from watchanalytics.models import Analytics
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SearchForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.http import JsonResponse
from .get_video_info import get_video_info
import random
from django.db.models import F,Q,ExpressionWrapper, fields
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.utils.decorators import method_decorator
from photos.models import Photo




def user_videos(request, username):
	user = get_object_or_404(User, username=username)
	photos=Photo.objects.filter(uploader=user).order_by('-upload_date')
	template = 'videos/user_videos.html'
	videos = VidStream.objects.filter(uploader=user).order_by('-upload_date')
	context = {
        'user': user,
        'videos': videos,
		'photos':photos}
	return render(request, template, context)


"""
@csrf_exempt
def like_video(request, video_id):
    video = VidStream.objects.get(id=video_id) 

    if request.user.is_authenticated:
        if request.user in video.likes.all():
            video.likes.remove(request.user)
            liked = False
        else:
            video.likes.add(request.user)
            liked = True
        return JsonResponse({'liked': liked, 'like_count': video.likes.count()})
   

"""""


@method_decorator(login_required,name='dispatch')
class LikedVideoView(View):
	@method_decorator(csrf_exempt)
	def dispatch(self,*args,**kwargs):
		return super().dispatch(*args,**kwargs)
	
	def post(self,request,video_id):
		if request.headers.get('x-requested') == 'XMLHttpRequest':
			video= get_object_or_404(VidStream,id=video_id)

			if request.user in video.likes.all():
				video.likes.remove(request.user)
				liked=False
			else:
				video.likes.add(request.user)
				liked=True

			response_data={'liked':liked,'like_count':video.likes.count()}
			return JsonResponse(response_data)
		return redirect('videos:video',video_id=video_id)

@login_required
def create_video(request):
	template= 'videos/video_create.html'
	if request.method == 'POST':
		video_form = VideoUploadForm(request.POST, request.FILES)
		if video_form.is_valid():
			video_instance = video_form.save(commit=False)
			video_instance.uploader = request.user
			video_instance.save()
			video_form.save_m2m()

			uploaded_video=request.FILES.get('video')
			video_id=video_instance.id


			thumb_generator(video_instance.video, video_instance)
			
			formatted_duration,formatted_size=get_video_info(uploaded_video.read())

			if formatted_duration is not None and formatted_size is not None:
				video_instance.duration=formatted_duration
				video_instance.size=formatted_size
				video_instance.save()
				messages.success(request,'success')
				return redirect('videos:video', video_id=video_id)
			else:
				messages.error(request,'Error getting video information.')
				return redirect('videos:video-list')
	
		else:
			messages.error(request, 'Error uploading video. Please check the form.')
	else:
		video_form = VideoUploadForm()

	return render(request,template,{'video_form': video_form} )





def videolist(request):
	videos=VidStream.objects.all()


	videos_per_page = 20

	paginator = Paginator(videos, videos_per_page)


	page = request.GET.get('page')


	try:
		video = paginator.page(page)

	except PageNotAnInteger:

		video = paginator.page(1)

	except EmptyPage:

		video = paginator.page(paginator.num_pages)

	return render(request, 'videos/video-list.html', {'videos':videos})



def search(request):
    video = []
    query = ''

    if 'title' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['title']
            video = VidStream.objects.filter(title__icontains=query)
    else:
        form = SearchForm()

    return render(request, 'videos/search.html', {'form': form, 'query': query, 'video': video})



def get_video(request, video_id):
	template='videos/video.html'
	video = VidStream.objects.get(id=video_id)
	comments=Comment.objects.filter(video=video_id)

	form=CommentForm()
	if request.method=='POST':
		form=CommentForm(request.POST)
		if form.is_valid:
			comment=form.save(commit=False)
			comment.user=request.user
			comment.video=video
			comment.save()
			return redirect('videos:video', video_id=video_id )	
			
	if not request.session.session_key:
		request.session.save()

	session_key= request.session.session_key
	is_views=Analytics.objects.filter(videoId=video_id, sesID=session_key)
	if is_views.count()== 0 and str(session_key) !="None":
		views=Analytics()
		views.sesID=session_key
		views.videoId=video			
		views.save()
		video.views += 1
		video.save()
		
	try:
		related_videos= random.sample(list(video.get_related_videos()),5)
	except Exception as e:
		print(f"Error retrieving related videos: {str(e)}")
		related_videos= []

	
	try:
		categories= random.sample(list(Category.objects.all()),10)
	except Exception as e:
		print(f"Error retrieving categories videos: {str(e)}")
		categories= []


	context={'comments':comments,'form':form ,'video':video, 'related_videos':related_videos,'categories':categories}
	return render(request,template,context)



def categoryView(request):
	template='videos/category.html'
	category= Category.objects.filter(status=0).order_by('name')
	context={'category':category}
	category_with_count = category.annotate(video_count=Count('vidstream'))
	context = {'category': category_with_count}
	
	category_per_page = 40
	paginator = Paginator(category, category_per_page)
	page = request.GET.get('page')

	try:
		category = paginator.page(page)
	except PageNotAnInteger:
		category = paginator.page(1)
	except EmptyPage:
		category = paginator.page(paginator.num_pages)
	
	return render(request, template, context)


def categorylist(request, slug):
	template='videos/category-list.html'
	if (Category.objects.filter(slug=slug, status=0)):
		videos=VidStream.objects.filter(category__slug=slug)
		category=Category.objects.filter(slug=slug).first()
		context={"videos":videos, 'category':category}
		videos_per_page = 20
		paginator = Paginator(videos, videos_per_page)
		page = request.GET.get('page')
		try:
			videos = paginator.page(page)
		except PageNotAnInteger:
			videos = paginator.page(1)
		except EmptyPage:
			videos = paginator.page(paginator.num_pages)
		
		
		return render(request, template, context)
	else:
		messages.warning(request, 'Category does not exist. You will be redirected to the category page momemntarily ')
		return redirect('video/category.html')


def most_viewed_videos(request):
    # Retrieve all video ordered by views in descending order
    most_viewed_videos = VidStream.objects.order_by('-views')

    context = {'most_viewed_videos': most_viewed_videos}
    return render(request, 'videos/most_viewed_videos.html', context)


def related_videos(request,id):
	video=get_object_or_404(VidStream,id=id)
	related_videos=VidStream.get_related_videos(video)
	context={'related_videos':related_videos,'video':video}
	return render(request,'videos/related_videos.html',context)


def trending_videos(request):
    # Define weights for each metric (adjust as needed)
    VIEW_WEIGHT = 0.8
    LIKE_WEIGHT = 0.15
    COMMENT_WEIGHT = 0.5

    MAX_VIEWS=1000000
    MAX_LIKES=1000000
    MAX_COMMENTS=1000000



    # Query videos and calculate normalized metrics
    videos =VidStream.objects.annotate(
        normalized_views=ExpressionWrapper(F('views') / MAX_VIEWS, output_field=fields.FloatField()),
        normalized_likes=ExpressionWrapper(F('likes') / MAX_LIKES, output_field=fields.FloatField()),
        normalized_comments=ExpressionWrapper(F('comments') / MAX_COMMENTS, output_field=fields.FloatField()),
    )

    # Calculate popularity score for each 
    videos = videos.annotate(
        popularity_score=(
            VIEW_WEIGHT * F('normalized_views') +
            LIKE_WEIGHT * F('normalized_likes') +
            COMMENT_WEIGHT * F('normalized_comments') 
        )
    )

    # Sort videos by popularity score (descending)
    trending_videos = videos.order_by('-popularity_score')

    # Pass trending videos to the template
    context = {'trending_videos': trending_videos}
    return render(request, 'videos/trending_videos.html', context)
