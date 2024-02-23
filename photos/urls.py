from . import views
from django.urls import path




urlpatterns= [
	#path('photo-list/', GeneralPhotoListView.as_view(template_name='photos/photo-list.html'),name='photo-list'),
	#path('photo_detail/<int:pk>',PhotoDetailView.as_view(template_name='photos/photo-detail.html'),name='photo-detail'),
	#path('<int:pk>delete/', PhotoDeleteView.as_view(template_name='photos/photo-confirm-delete.html'),name='photo-delete'),
	#path('user/<str:username>',UserPhotoListView.as_view(template_name='photos/user-photos-list.html'),name='user-photo'),
	path('new/',views.create_photo,name='photo_create'),
    path('photo/<int:id>/',views.get_photo, name='photo'),
    path('photos/', views.all_photos,name='photos')


]