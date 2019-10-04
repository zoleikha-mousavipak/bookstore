from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views


app_name = "accounts"

urlpatterns = [
     path('signup/', views.signup, name='signup'),
     path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
     path('api/token-auth/', obtain_auth_token, name='api_token_auth'),


]
