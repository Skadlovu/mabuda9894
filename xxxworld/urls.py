from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static 
from django.contrib.auth import views as auth_views
from profiles import views as profiles_views
from.views import assist
from stream import routing
from profiles.views import password

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('donations.urls')),
    path('',include('videos.urls')),
    path('',include('photos.urls')),
    #path('',include('stream.urls')),
    path('profiles/',profiles_views.profile, name="profile"),
    path('register/',profiles_views.register, name="register"),
    path('login', auth_views.LoginView.as_view(template_name='profiles/login.html'), name="login"),
    path('logout',auth_views.LogoutView.as_view(template_name='profiles/logout.html'), name="logout"),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='profiles/password_reset.html'), name='password_reset'),
    path('',auth_views.PasswordChangeDoneView.as_view(), name='password_change'),
    path('assist/',assist, name='assist'),
    path('payfast/', include('payfast.urls')),
    #path('ws/', include('stream.routing.websocket_urlpatterns')),
    #path('password_reset/',password, name='password_reset' ),
    
    
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

