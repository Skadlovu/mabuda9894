from . import views
from django.urls import path



app_name='videos'

urlpatterns= [
	path('videos/new/', views.create_video, name='video_create'),
	path('videos/search/',views.search, name='search'),
	path('videos/video/<video_id>', views.get_video, name='video'),
	path('videos/category/', views.categoryView, name='category'),
	path('videos/category-list <str:slug>/', views.categorylist,name='category-list'),
	path('', views.videolist, name='video-list'),
    path('videos/trending_videos', views.trending_videos, name='trending_videos'),
    path('videos/most_viewed_videos', views.most_viewed_videos, name='most_viewed_videos'),
    path('videos/video/<int:video_id>', views.LikedVideoView.as_view, name='like_video'),
    path('videos/user/<str:username>',views.user_videos,name='user_videos'),
    path('videos/related_videos/<int:id>',views.related_videos,name='related_videos'),
    #path('videos/video/<int:video_id>', views.submit_comment, name='submit_comment'),
 
    


]



	#path('videos/category/', CategoryListView.as_view(template_name='videos/category.html'),name='category'),
# path('videos/video/<int:pk>/',VideoDetailView.as_view(),name='video'),
# path('videos/new/', VideoCreateView.as_view(template_name='videos/video_create.html'),name='video_create'),
	#path('videos/<int:pk>delete/', VideoDeleteView.as_view(),name='video-delete'),
# path('', GeneralVideoListView.as_view(),name='video-list'),
