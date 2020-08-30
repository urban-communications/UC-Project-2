from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView

from clientApp.models import Client


class HomeView(TemplateView):
    template_name = 'home.html'

class ClientProfileView(DetailView):
    model = Client
    template_name = 'client_profile.html'
    context_object_name = 'client'