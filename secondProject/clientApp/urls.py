from django.urls import path
from django.contrib.auth.models import User

from . import views
from secondProject.views import ClientRegistration

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('signup/', ClientRegistration.as_view(), name='client_signup'),
    path('profile/<slug:pk>/', views.ClientProfileView.as_view(), name='client_profile'),
]

app_name = 'clientApp'