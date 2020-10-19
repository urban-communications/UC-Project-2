from django.shortcuts import redirect, render
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth import update_session_auth_hash, login, authenticate
from django.urls import reverse
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


from clientApp.models import (
    User,
    Client,
    Operator,
    Employee
)
from clientApp.forms import (
    UserRegistrationForm,
    ClientRegistrationForm,
    OperatorRegistrationForm,
    EmployeeRegistrationForm
)


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
            html_content = f"""<div>
                <em>This is an automated e-mail - please do not reply to this address</em><br>
                <h2>PRIVATE & CONFIDENTIAL</h2>
                <p>Dear {form_client.cleaned_data['client_name']}, </p>
                <p>Welcome and congrats on becoming a member of the Urban Communications Family.</p>
                <p>We are glad to inform you that your account has been registered successfully.</p><br>

                <p><b> Your account credentials are as follow:</b></p>
                <p><b>Username:</b> {form_user.cleaned_data['username']} <br> 
                <b>Password:</b> {form_user.cleaned_data['password1']}</p><br>

                <p>You can now login by visiting our website at: <a href="http://www.app.urban-communications.co.uk/">http://www.app.urban-communications.co.uk</a> </p> <br>
                <b>Things you can do by login:<br>
                <ul>
                    <li>You can view the list of operators associated with you</li>
                    <li>You can approve or decline any holiday request from your operator</li>
                    <li>You can give feedback to your operator and view it</li>
                    <li>You can send a message to your operator and Urban Communications</li>
                    <li>You can view your invoices from Urban Communications</li>
                    <li>You can also view your profile information</li>
                </ul> <br>
                <p>Kind Regards,</p>
                <p>Urban Communications</p>
                <a href="http://www.app.urban-communications.co.uk/">admin@urban-communications.co.uk</a>

                </div>"""
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
                html_content = f"""<div>
                <em>This is an automated e-mail - please do not reply to this address</em><br>
                <h2>PRIVATE & CONFIDENTIAL</h2>
                <p>Dear {name}, </p>
                <p>Welcome and congrats on becoming a member of the Urban Communications Family.</p>
                <p>We are glad to inform you that your account has been registered successfully.</p><br>


                <p><b> Your account credentials are as follow:</b></p>
                <p><b>Username:</b> {form_user.cleaned_data['username']} <br> 
                <b>Password:</b> {form_user.cleaned_data['password1']}</p><br>


                <p>You can now login by visiting our website at: <a href="http://www.app.urban-communications.co.uk/">http://www.app.urban-communications.co.uk</a> </p> <br>
                <b>Things you can do by login:<br>
                <ul>
                    <li>You can request your holidays and track its status</li>
                    <li>You can check your feedbacks</li>
                    <li>You can view and upload your documents</li>
                    <li>You can view a message from Urban Communications and you associated client</li>
               </ul> <br>
                <p>Kind Regards,</p>
                <p>Urban Communications</p>
                <a href="http://www.app.urban-communications.co.uk/">admin@urban-communications.co.uk</a>

                </div>"""
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


class EmployeeRegistration(TemplateView):
    template_name = 'employee_registration.html'

    def get(self, request):
        if(request.user.is_staff):
            user_form = UserRegistrationForm()
            employee_form = EmployeeRegistrationForm()
            context = {
                'user_form': user_form,
                'employee_form': employee_form
            }
            return render(request, self.template_name, context)
        else:
            return redirect('clientApp:home')

    def post(self, request):
        if request.user.is_staff:
            context = {}
            form_user = UserRegistrationForm(request.POST)
            form_employee = EmployeeRegistrationForm(
                request.POST, request.FILES)

            if form_employee.is_valid() and form_user.is_valid():
                data = form_user.save()
                name = form_user.cleaned_data['first_name'] + \
                    ' ' + form_user.cleaned_data['last_name']
                new_employee = Employee(
                    user_name=data,
                    job_designation=form_employee.cleaned_data['job_designation'],
                    employee_name=name,
                    contact_number=form_employee.cleaned_data['contact_number'],
                    date_of_birth=form_employee.cleaned_data['date_of_birth'],
                    address=form_employee.cleaned_data['address'],
                    total_leaves=form_employee.cleaned_data['total_leaves'],
                    available_leaves=form_employee.cleaned_data['total_leaves'],
                    profile_picture=form_employee.cleaned_data['profile_picture']
                )
                new_employee.save()
                messages.success(request, "Employee created successfully.")

                # send an email
                subject, from_email, to = f"{name} signed up Successfully", settings.EMAIL_HOST_USER, form_user.cleaned_data[
                    'email']
                text_content = "Your account has been registered successfully"
                html_content = f"""<div>
                <em>This is an automated e-mail - please do not reply to this address</em><br>
                <h2>PRIVATE & CONFIDENTIAL</h2>
                <p>Dear {name}, </p>
                <p>Welcome and congrats on becoming a member of the Urban Communications Family.</p>
                <p>We are glad to inform you that your account has been registered successfully.</p><br>


                <p><b> Your account credentials are as follow:</b></p>
                <p><b>Username:</b> {form_user.cleaned_data['username']} <br> 
                <b>Password:</b> {form_user.cleaned_data['password1']}</p><br>


                <p>You can now login by visiting our website at: <a href="http://www.app.urban-communications.co.uk/">http://www.app.urban-communications.co.uk</a> </p> <br>
                <b>Things you can do by login:<br>
                <ul>
                    <li>You can request your holidays and track its status</li>
                    <li>You can check your feedbacks</li>
                    <li>You can view and upload your documents</li>
                    <li>You can view a message from Urban Communications</li>
                </ul> <br>
                <p>Kind Regards,</p>
                <p>Urban Communications</p>
                <a href="http://www.app.urban-communications.co.uk/">admin@urban-communications.co.uk</a>

                </div>"""
                msg = EmailMultiAlternatives(
                    subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                messages.success(
                    request, "Email with login credientials has been sent successfully.")
                return HttpResponseRedirect(request.path_info)
            else:
                context['user_form'] = form_user
                context['employee_form'] = form_employee
            return render(request, self.template_name, context)
        else:
            return redirect('clientApp:home')
