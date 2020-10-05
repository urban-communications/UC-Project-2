from django.shortcuts import redirect, render
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth import update_session_auth_hash, login, authenticate
from django.urls import reverse
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


from clientApp.models import User, Client, Operator
from clientApp.forms import UserRegistrationForm, ClientRegistrationForm, OperatorRegistrationForm


def password_change_form(request):
    pass


def login_redirect(request):
    if request.user.is_authenticated:
        return redirect(reverse('clientApp:home'))


class ClientRegistration(TemplateView):
    template_name = 'client_registration.html'

    def get(self, request):
        user_form = UserRegistrationForm()
        client_form = ClientRegistrationForm()
        context = {
            'user_form': user_form,
            'client_form': client_form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        context = {}
        form_user = UserRegistrationForm(request.POST)
        form_client = ClientRegistrationForm(request.POST, request.FILES)
        if form_client.is_valid() and form_user.is_valid():
            data = form_user.save()
            new_client = Client(
                user_name=data,
                client_name=form_client.cleaned_data['client_name'],
                client_type=form_client.cleaned_data['client_type'],
                contact_number=form_client.cleaned_data['contact_number'],
                address=form_client.cleaned_data['address'],
                profile_picture=form_client.cleaned_data['profile_picture']
            )
            new_client.save()
            messages.success(request, "Client created successfully.")

            # send an email
            subject, from_email, to = f"{form_client.cleaned_data['client_name']} signed up Successfully", settings.EMAIL_HOST_USER, form_user.cleaned_data[
                'email']
            text_content = "Your account has been registered successfully"
            html_content = f"<p>Hi, <br> Your account has been registered successfully. <br> Your account credientials are as follow. <br> Username: {form_user.cleaned_data['username']} <br> Password: {form_user.cleaned_data['password1']} <br> <br> you can now login by visiting our website at: <a> https://urbancommunications.herokuapp.com/ </a> </p>"
            msg = EmailMultiAlternatives(
                subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            messages.success(
                request, "Email with login credientials has been sent successfully.")
            return HttpResponseRedirect(request.path_info)
        else:
            context['user_form'] = form_user
            context['client_form'] = form_client
        return render(request, self.template_name, context)


class OperatorRegistration(TemplateView):
    template_name = 'operator_registration.html'

    def get(self, request):
        if(request.user.is_staff):
            user_form = UserRegistrationForm()
            operator_form = OperatorRegistrationForm()
            context = {
                'user_form': user_form,
                'operator_form': operator_form
            }
            return render(request, self.template_name, context)
        else:
            return redirect('clientApp:home')

    def post(self, request):
        if request.user.is_staff:
            context = {}
            form_user = UserRegistrationForm(request.POST)
            form_operator = OperatorRegistrationForm(
                request.POST, request.FILES)

            if form_operator.is_valid() and form_user.is_valid():
                data = form_user.save()
                name = form_user.cleaned_data['first_name'] + \
                    ' ' + form_user.cleaned_data['last_name']
                new_operator = Operator(
                    user_name=data,
                    client_id=form_operator.cleaned_data['client_id'],
                    operator_name=name,
                    contact_number=form_operator.cleaned_data['contact_number'],
                    date_of_birth=form_operator.cleaned_data['date_of_birth'],
                    address=form_operator.cleaned_data['address'],
                    total_leaves=form_operator.cleaned_data['total_leaves'],
                    available_leaves=form_operator.cleaned_data['total_leaves'],
                    profile_picture=form_operator.cleaned_data['profile_picture']
                )
                new_operator.save()
                messages.success(request, "Operator created successfully.")

                # send an email
                subject, from_email, to = f"{name} signed up Successfully", settings.EMAIL_HOST_USER, form_user.cleaned_data[
                    'email']
                text_content = "Your account has been registered successfully"
                html_content = f"<p>Hi, <br> Your account has been registered successfully. <br> Your account credientials are as follow. <br> Username: {form_user.cleaned_data['username']} <br> Password: {form_user.cleaned_data['password1']} <br> <br> you can now login by visiting our website at: <a> https://urbancommunications.herokuapp.com/ </a> </p>"
                msg = EmailMultiAlternatives(
                    subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                messages.success(
                    request, "Email with login credientials has been sent successfully.")
                return HttpResponseRedirect(request.path_info)
            else:
                context['user_form'] = form_user
                context['operator_form'] = form_operator
            return render(request, self.template_name, context)
        else:
            return redirect('clientApp:home')
