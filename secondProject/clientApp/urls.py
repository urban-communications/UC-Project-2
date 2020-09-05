from django.urls import path
from django.contrib.auth.models import User

from . import views
from secondProject.views import ClientRegistration, OperatorRegistration

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('signup-operator/', OperatorRegistration.as_view(), name='operator_signup'),
    path('signup/', ClientRegistration.as_view(), name='client_signup'),
    path('admin-signup/', ClientRegistration.as_view(), name='admin_client_signup'),
    path('profile/<slug:pk>/', views.ClientProfileView.as_view(), name='client_profile'),
    path('feedback/', views.FeedbackView.as_view(), name='client_feedback'),
    path('feedback/list/', views.ListClientFeedbackView.as_view(), name='client_feedback_list'),
]

app_name = 'clientApp'