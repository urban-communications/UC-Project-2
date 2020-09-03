from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.conf.urls.static import static

from secondProject import views

urlpatterns = [
    path('', views.login_redirect),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('client/', include('clientApp.urls', namespace='clientApp')),
    path('accounts/password_change/',
         views.password_change_form, name='password_change'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
