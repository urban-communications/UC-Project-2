from django.shortcuts import redirect, render
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth import update_session_auth_hash, login, authenticate
from django.urls import reverse
from django.views.generic import TemplateView

from clientApp.models import User, Client, Operator
from clientApp.forms import UserRegistrationForm, ClientRegistrationForm, OperatorRegistrationForm


def password_change_form(request):
    pass


class ClientRegistration(TemplateView):
    template_name = 'client_registration.html'

    def get(self, request):
        user_form = UserRegistrationForm()
        client_form = ClientRegistrationForm()
        context ={
            'user_form' : user_form,
            'client_form' : client_form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        context = {}
        form_user = UserRegistrationForm(request.POST)
        form_client = ClientRegistrationForm(request.POST, request.FILES)
        if form_client.is_valid() and form_user.is_valid():
            data = form_user.save()
            name = form_user.cleaned_data['first_name'] + ' ' + form_user.cleaned_data['last_name']
            new_client = Client(
                user_name = data,
                client_name = name,
                client_type = form_client.cleaned_data['client_type'],
                contact_number = form_client.cleaned_data['contact_number'],
                date_of_birth = form_client.cleaned_data['date_of_birth'],
                address = form_client.cleaned_data['address'],
                profile_picture = form_client.cleaned_data['profile_picture']
            )
            new_client.save()
            return redirect('login')
        else:
            context['user_form'] = form_user
            context['client_form'] = form_client
        return render(request, self.template_name, context)

