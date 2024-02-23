from django.urls import path
from .views import donate

app_name = 'donations'  

urlpatterns = [
    path('donate/', donate, name='donate'),
    #path('thank-you/', thank_you_view, name='thank_you'),
]
