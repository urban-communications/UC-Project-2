from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.edit import FormView
from clientApp.models import Operator, Feedback
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from clientApp.forms import (
    FeedbackForm,
    LeaveForm,
    OperatorDocumentsForm,
    ClientSendMessageForm,
    AdminSendMessageForm,
    AdminSendMessageToOperatorForm,
    ClientSendMessageToAdminForm,
    ClientInvoiceForm,
    EmployeeDocumentsForm,
    EmployeeHolidayForm,
    EmployeeFeedbackForm
)
from django.contrib.auth.models import User
from clientApp.models import (
    Client,
    Leave,
    OperatorDocuments,
    MessageQuries,
    Invoices,
    EmployeeDocuments,
    EmployeeHoliday,
    EmployeeFeedback
)


class HomeView(TemplateView):
    template_name = 'home.html'

    def get(self, request):
        adminChatForm = None
        adminChatOperatorForm = None
        clientChatForm = None
        clientTotalOperator = None
        clientChatAdmin = None
        adminTotalOperator = None
        adminTotalClient = None
        pendingHolidayCount = None
        messageCount = None
        operatorAdminMessageCount = None
        invoiceCount = None
        feedbackCount = None
        admin = User.objects.get(is_superuser=True, is_staff=True)
        adminClientMessageCountList = []
        pendingHolidayEmployeeCount = None

        if request.user.is_staff:
            adminChatForm = AdminSendMessageForm(request)
            adminChatOperatorForm = AdminSendMessageToOperatorForm()
            adminTotalOperator = Operator.objects.all().order_by('operator_name')
            adminTotalClient = Client.objects.all().order_by('client_name')
            pendingHolidayCount = Leave.objects.filter(
                leave_status='Pending', read_by_admin=False).count()
            feedbackCount = Feedback.objects.filter(
                read_by_admin=False).count()
            pendingHolidayEmployeeCount = EmployeeHoliday.objects.filter(
                leave_status='Pending', read_by_admin=False).count()

            for client in adminTotalClient:
                adminClientMessageCount = MessageQuries.objects.filter(
                    client_id=client.client_user_id, admin_id=request.user.id, read_by_admin=False).count()
                data = {
                    'client_id': client.client_user_id,
                    'count': adminClientMessageCount
                }
                adminClientMessageCountList.append(data)

        if hasattr(request.user, 'client'):
            clientChatForm = ClientSendMessageForm(request)
            clientChatAdmin = ClientSendMessageToAdminForm()
            clientTotalOperator = Operator.objects.filter(
                client_id=request.user.client.client_user_id).order_by('operator_name')
            pendingHolidayCount = Leave.objects.filter(
                leave_status='Pending', client_id=request.user.client.client_user_id, read_by_client=False).count()
            messageCount = MessageQuries.objects.filter(
                client_id=request.user.client.client_user_id, admin_id=admin.id, read_by_client=False).count()
            invoiceCount = Invoices.objects.filter(
                client_id=request.user.client.client_user_id, read_by_client=False).count()

        if hasattr(request.user, 'operator'):
            pendingHolidayCount = Leave.objects.filter(
                leave_status='Pending', operator_id=request.user.operator.operator_user_id, read_by_operator=False).count()
            messageCount = MessageQuries.objects.filter(
                operator_id=request.user.operator.operator_user_id, client_id=request.user.operator.client_id.client_user_id, read_by_operator=False).count()
            operatorAdminMessageCount = MessageQuries.objects.filter(
                operator_id=request.user.operator.operator_user_id, admin_id=admin.id, read_by_operator=False).count()

            feedbackCount = Feedback.objects.filter(
                operator_id=request.user.operator.operator_user_id, read_by_operator=False).count()

        if hasattr(request.user, 'employee'):
            pendingHolidayCount = EmployeeHoliday.objects.filter(
                leave_status='Pending', employee_id=request.user.employee.employee_user_id, read_by_employee=False).count()
            feedbackCount = EmployeeFeedback.objects.filter(
                employee_id=request.user.employee.employee_user_id, read_by_employee=False).count()

        context = {
            'clientChatForm': clientChatForm,
            'clientChatAdmin': clientChatAdmin,
            'adminChatForm': adminChatForm,
            'adminChatOperator': adminChatOperatorForm,
            'totalOperator': clientTotalOperator,
            'adminAccount': admin,
            'adminTotalOperator': adminTotalOperator,
            'adminTotalClient': adminTotalClient,
            'pendingLeaveCount': pendingHolidayCount,
            'invoiceCount': invoiceCount,
            'messageCount': messageCount,
            'operatorAdminMessageCount': operatorAdminMessageCount,
            'feedbackCount': feedbackCount,
            'adminClientMessageCountList': adminClientMessageCountList,
            'pendingHolidayEmployeeCount': pendingHolidayEmployeeCount
        }
        return render(request, self.template_name, context)

    def post(self, request):
        if request.user.is_staff:
            adminChatForm = AdminSendMessageForm(request, request.POST)
            adminChatOperatorForm = AdminSendMessageToOperatorForm(
                request.POST)
            if adminChatForm.is_valid():
                data = adminChatForm.save(commit=False)
                data.admin_id = request.user
                data.sender = 'Company'
                data.read_by_admin = True
                data.save()
                messages.success(request, "Your message has been sent.")
                return HttpResponseRedirect(request.path_info)
            if adminChatOperatorForm.is_valid():
                data = adminChatOperatorForm.save(commit=False)
                data.admin_id = request.user
                data.sender = 'Company'
                data.read_by_admin = True
                data.save()
                messages.success(request, "Your message has been sent.")
                return HttpResponseRedirect(request.path_info)
        elif request.user.client:
            clientChatForm = ClientSendMessageForm(request, request.POST)
            clientChatAdmin = ClientSendMessageToAdminForm(request.POST)
            if clientChatForm.is_valid():
                data = clientChatForm.save(commit=False)
                data.client_id = request.user.client
                data.sender = 'Client'
                data.read_by_client = True
                data.save()
                messages.error(request, "Your message has been sent.")
                return HttpResponseRedirect(request.path_info)
            if clientChatAdmin.is_valid():
                companyUser = User.objects.get(
                    is_staff=True, is_superuser=True)
                data = clientChatAdmin.save(commit=False)
                data.client_id = request.user.client
                data.sender = 'Client'
                data.admin_id = companyUser
                data.read_by_client = True
                data.save()
                messages.error(request, "Your message has been sent.")
                return HttpResponseRedirect(request.path_info)
        else:
            messages.error(request, "Failed to send message. Try Again")
            return HttpResponseRedirect(request.path_info)


class ClientProfileView(DetailView):
    model = Client
    template_name = 'client_profile.html'
    context_object_name = 'client'


class OperatorProfileView(DetailView):
    model = Operator
    template_name = 'operator_profile.html'
    context_object_name = 'operator'


class FeedbackView(TemplateView):
    template_name = 'client_feedback.html'

    def get(self, request):
        feedback = FeedbackForm(request)
        context = {
            'feedback': feedback
        }
        return render(request, self.template_name, context)

    def post(self, request):
        if request.user.client:
            context = {}
            feedback_form = FeedbackForm(request, request.POST)
            if feedback_form.is_valid():
                data = feedback_form.save(commit=False)
                data.client_id = self.request.user.client
                data.save()
                messages.success(
                    request, "Your feedback has been submitted. Thank you")
                return HttpResponseRedirect(request.path_info)
            else:
                context['feedback_form'] = feedback_form()
            return render(request, self.template_name, context)
        else:
            return redirect('clientApp:home')


class ListClientFeedbackView(ListView):
    template_name = 'client_feedback_list.html'
    model = Feedback
    context_object_name = 'feedback_list'
    paginate_by = 5

    def get_queryset(self):
        # for search feedback
        query = self.request.GET.get("q")
        if query:
            return Feedback.objects.filter(client_id=self.request.user.client.client_user_id, rating__icontains=query)

        return Feedback.objects.filter(client_id=self.request.user.client.client_user_id).order_by('-created_at')


class ListOperatorFeedbackView(ListView):
    template_name = 'operator_feedback_list.html'
    model = Feedback
    context_object_name = 'feedback_list'
    paginate_by = 10

    def get_queryset(self):
        Feedback.objects.filter(operator_id=self.request.user.operator.operator_user_id,
                                read_by_operator=False).update(read_by_operator=True)

        # for search feedback
        query = self.request.GET.get("q")
        if query:
            return Feedback.objects.filter(operator_id=self.request.user.operator.operator_user_id, rating__icontains=query)

        return Feedback.objects.filter(operator_id=self.request.user.operator.operator_user_id).order_by('-created_at')


class ListAdminFeedbackView(ListView):
    template_name = 'admin_feedback_list.html'
    model = Feedback
    context_object_name = 'feedback_list'
    paginate_by = 5

    def get_queryset(self):
        Feedback.objects.filter(read_by_admin=False).update(read_by_admin=True)

        # for search feedback
        query = self.request.GET.get("q")
        if query:
            return Feedback.objects.filter(rating__icontains=query)

        return Feedback.objects.all().order_by('-created_at')


class OperatorLeaveRequest(TemplateView):
    template_name = 'operator_leave_request.html'

    def get(self, request):
        form = LeaveForm()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        context = {}
        if request.user.operator:
            form = LeaveForm(request.POST)
            if form.is_valid():
                # Calculate no. of holidays
                day = form.cleaned_data['to_date'] - \
                    form.cleaned_data['from_date']
                total_days = day.days
                if(total_days > 0):
                    total_days = total_days + 1
                if(total_days == 0):
                    total_days = 1

                if(total_days >= 1):
                    data = form.save(commit=False)
                    data.no_of_days = total_days
                    data.operator_id = self.request.user.operator
                    data.client_id = self.request.user.operator.client_id
                    data.save()
                    messages.success(
                        request, "Your holiday request has been submitted! We will get back in touch with you soon. Thank you")
                else:
                    messages.error(request, "Kindly select a valid date range")
                return HttpResponseRedirect(request.path_info)
            else:
                context['form'] = form()
                return render(request, self.template_name, context)
        else:
            return redirect('clientApp:home')


class OperatorLeaveList(ListView):
    template_name = 'operator_leave_list.html'
    model = Leave
    context_object_name = 'leave_list'
    paginate_by = 10

    def get_queryset(self):
        action = self.request.path.split('/')[-1]
        if action == "Pending":
            Leave.objects.filter(operator_id=self.request.user.operator.operator_user_id,
                                 leave_status="Pending", read_by_operator=False).update(read_by_operator=True)
        return Leave.objects.filter(operator_id=self.request.user.operator.operator_user_id, leave_status=action).order_by('-created_at')


class OperatorLeaveDetail(DetailView):
    model = Leave
    template_name = 'leave_detail.html'
    context_object_name = 'leave'


class ClientLeaveList(ListView):
    template_name = 'client_leave_list.html'
    model = Leave
    context_object_name = 'leave_list'
    paginate_by = 10

    def get_queryset(self):
        action = self.request.path.split('/')[-1]
        if action == "Pending":
            Leave.objects.filter(client_id=self.request.user.client.client_user_id,
                                 leave_status="Pending", read_by_client=False).update(read_by_client=True)
        return Leave.objects.filter(client_id=self.request.user.client.client_user_id, leave_status=action).order_by('-created_at')


def leave_approve(request, pk):
    if request.user.is_staff:
        leave = Leave.objects.get(leave_id=pk)
        leave.admin_leave_status = "Approved"
        leave.updated_at = timezone.now()
        if leave.client_leave_status == "Approved":
            leave.leave_status = "Approve"
            # send an email
            subject, from_email, to = "Holiday request approved", settings.EMAIL_HOST_USER, leave.operator_id.user_name.email
            text_content = "Operator Holiday request has been approved."
            html_content = f"""<p>Hi {leave.operator_id.operator_name}, <br> 
                Your holiday request has been Approved. <br> 
                Your holiday summary is as follow. <br> 
                From: {leave.from_date} <br> 
                To: {leave.to_date} <br>
                Total Holidays: {leave.no_of_days} <br>
                Reason: {leave.reason} <br>
                Leave final status: {leave.leave_status} <br> 
                Client Action: {leave.client_leave_status} <br> 
                Company Action: {leave.admin_leave_status} <br> <br>
                You can login by visiting our website for more details: <a> https://urbancommunications.herokuapp.com/ </a> </p>
                """
            msg = EmailMultiAlternatives(
                subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            messages.success(
                request, "Email send to operator successfully.")
        leave.save()
        messages.success(
            request, "Holiday request has been approved. Thank you.")
        return redirect('clientApp:home')
    if hasattr(request.user, 'client'):
        leave = Leave.objects.get(leave_id=pk)
        leave.client_leave_status = "Approved"
        leave.updated_at = timezone.now()
        if leave.admin_leave_status == "Approved":
            leave.leave_status = "Approve"
            # send an email
            subject, from_email, to = "Holiday request approved", settings.EMAIL_HOST_USER, leave.operator_id.user_name.email
            text_content = "Operator Holiday request has been approved."
            html_content = f"""<p>Hi {leave.operator_id.operator_name}, <br> 
                Your holiday request has been Approved. <br> 
                Your holiday summary is as follow. <br> 
                From: {leave.from_date} <br> 
                To: {leave.to_date} <br>
                Total Holidays: {leave.no_of_days} <br>
                Reason: {leave.reason} <br>
                Leave final status: {leave.leave_status} <br> 
                Client Action: {leave.client_leave_status} <br> 
                Company Action: {leave.admin_leave_status} <br> <br>
                You can login by visiting our website for more details: <a> https://urbancommunications.herokuapp.com/ </a> </p>
                """
            msg = EmailMultiAlternatives(
                subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            messages.success(
                request, "Email send to operator successfully.")
        leave.save()
        messages.success(
            request, "Holiday request has been approved. Thank you.")
        return redirect('clientApp:home')
    else:
        messages.success(
            request, "You don't have valid permission to approve holiday request.")
        return redirect('clientApp:home')


def leave_reject(request, pk):
    if request.user.is_staff or hasattr(request.user, 'client'):
        leave = Leave.objects.get(leave_id=pk)
        leave.updated_at = timezone.now()
        if request.user.is_staff:
            leave.admin_leave_status = "Declined"
        if hasattr(request.user, 'client'):
            leave.client_leave_status = "Declined"
        leave.leave_status = "Decline"
        leave.save()
        messages.success(
            request, "Holiday request has been declined. Thank you.")

        # send an email
        subject, from_email, to = "Holiday request declined", settings.EMAIL_HOST_USER, leave.operator_id.user_name.email
        text_content = "Operator Holiday request has been declined."
        html_content = f"""<p>Hi {leave.operator_id.operator_name}, <br> 
            Your holiday request has been declined. <br> 
            Your holiday summary is as follow. <br> 
            From: {leave.from_date} <br> 
            To: {leave.to_date} <br>
            Total Holidays: {leave.no_of_days} <br>
            Reason: {leave.reason} <br>
            Leave final status: {leave.leave_status} <br> 
            Client Action: {leave.client_leave_status} <br> 
            Company Action: {leave.admin_leave_status} <br> <br>
            You can login by visiting our website for more details: <a> https://urbancommunications.herokuapp.com/ </a> </p>"""
        msg = EmailMultiAlternatives(
            subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        messages.success(
            request, "Email send to operator successfully.")

        return redirect('clientApp:home')
    else:
        messages.success(
            request, "You don't have valid permission to decline holiday request.")
        return redirect('clientApp:home')


class AdminLeaveList(ListView):
    template_name = 'client_leave_list.html'
    model = Leave
    context_object_name = 'leave_list'
    paginate_by = 10

    def get_queryset(self):
        action = self.request.path.split('/')[-1]
        if action == "Pending":
            Leave.objects.filter(leave_status="Pending",
                                 read_by_admin=False).update(read_by_admin=True)

        query = self.request.GET.get("q")
        if query:
            return Leave.objects.filter(leave_status=action,  operator_id__operator_name__icontains=query)
        return Leave.objects.filter(leave_status=action).order_by('-created_at')


class OperatorDocumentsUpload(FormView):
    form_class = OperatorDocumentsForm
    template_name = 'operator_documents_upload.html'
    success_url = reverse_lazy("clientApp:home")
    context_object_name = 'document'

    def post(self, request):
        form = OperatorDocumentsForm(request.POST, request.FILES)
        files = request.FILES.getlist('documents')
        if form.is_valid():
            for doc in files:
                document = OperatorDocuments(
                    operator_id=request.user.operator,
                    doc_title=doc.name,
                    documents=doc
                )
                document.save()
                messages.success(request, "Uploaded Successfully.")
            return HttpResponseRedirect(request.path_info)
        else:
            messages.error(request, "Failed to upload: Invalid files.")
            form = OperatorDocumentsForm()


class OperatorDocumentsList(ListView):
    template_name = 'operator_documents_list.html'
    model = OperatorDocuments
    context_object_name = 'documents'
    paginate_by = 10

    def get_queryset(self):
        return OperatorDocuments.objects.filter(operator_id=self.request.user.operator.operator_user_id)


def operatorDocumetDelete(request, pk):
    if hasattr(request.user, 'operator'):
        document = OperatorDocuments.objects.get(doc_id=pk)
        if document:
            document.documents.delete()
            document.delete()
            messages.success(request, "Deleted Successfully.")
            return HttpResponseRedirect(reverse('clientApp:operator_document_list'))
        else:
            messages.error(request, "Error while deleting the file.")
            return render(request, 'operator_documents_list.html')

    if hasattr(request.user, 'employee'):
        document = EmployeeDocuments.objects.get(doc_id=pk)
        if document:
            document.documents.delete()
            document.delete()
            messages.success(request, "Deleted Successfully.")
            return HttpResponseRedirect(reverse('clientApp:employee_document_list'))
        else:
            messages.error(request, "Error while deleting the file.")
            return render(request, 'operator_documents_list.html')


class ClientOperatorList(ListView):
    model = Operator
    template_name = "client_operator_list.html"
    context_object_name = 'operator_list'
    paginate_by = 10

    def get_queryset(self):
        return Operator.objects.filter(client_id=self.request.user.client.client_user_id)


class ClientOperatorDocumentsList(ListView):
    template_name = 'client_operator_documents_list.html'
    model = OperatorDocuments
    context_object_name = 'documents'
    paginate_by = 10

    def get_queryset(self):
        path = self.request.path_info.split('/')
        return OperatorDocuments.objects.filter(operator_id=path[-1])


class OperatorViewClientMessages(ListView):
    template_name = 'operator_view_messages_client.html'
    model = MessageQuries
    context_object_name = 'message_list'
    paginate_by = 20

    def get_queryset(self):
        MessageQuries.objects.filter(operator_id=self.request.user.operator.operator_user_id, client_id=self.request.user.operator.client_id.client_user_id,
                                     read_by_operator=False).update(read_by_operator=True)
        return MessageQuries.objects.filter(operator_id=self.request.user.operator.operator_user_id, client_id=self.request.user.operator.client_id.client_user_id).order_by('-created_at')


class OperatorViewAdminMessages(ListView):
    template_name = 'operator_view_message_admin.html'
    model = MessageQuries
    context_object_name = 'message_list'
    paginate_by = 20

    def get_queryset(self):
        admin = User.objects.get(is_staff=True, is_superuser=True)
        MessageQuries.objects.filter(operator_id=self.request.user.operator.operator_user_id, admin_id=admin.id,
                                     read_by_operator=False).update(read_by_operator=True)
        return MessageQuries.objects.filter(operator_id=self.request.user.operator.operator_user_id, admin_id=admin.id).order_by('-created_at')


class ClientOperatorViewMessage(ListView):
    template_name = 'client_view_message_operator.html'
    model = MessageQuries
    context_object_name = 'message_list'
    paginate_by = 20

    def get_queryset(self):
        operator_id = self.request.path.split('/')[-1]
        return MessageQuries.objects.filter(operator_id=operator_id, client_id=self.request.user.client.client_user_id).order_by('-created_at')


class ClientAdminViewMessage(ListView):
    template_name = 'client_admin_view_message.html'
    model = MessageQuries
    context_object_name = 'message_list'
    paginate_by = 20

    def get_queryset(self):
        admin_id = self.request.path.split('/')[-1]
        MessageQuries.objects.filter(client_id=self.request.user.client.client_user_id,
                                     admin_id=admin_id, read_by_client=False).update(read_by_client=True)
        return MessageQuries.objects.filter(client_id=self.request.user.client.client_user_id, admin_id=admin_id).order_by('-created_at')


class AdminClientViewMessage(ListView):
    template_name = 'client_admin_view_message.html'
    model = MessageQuries
    context_object_name = 'message_list'
    paginate_by = 20

    def get_queryset(self):
        client_user_id = self.request.path.split('/')[-1]
        MessageQuries.objects.filter(
            client_id=client_user_id, admin_id=self.request.user.id, read_by_admin=False).update(read_by_admin=True)
        return MessageQuries.objects.filter(client_id=client_user_id, admin_id=self.request.user.id).order_by('-created_at')


class AdminOperatorViewMessage(ListView):
    template_name = 'client_view_message_operator.html'
    model = MessageQuries
    context_object_name = 'message_list'
    paginate_by = 20

    def get_queryset(self):
        operator_id = self.request.path.split('/')[-1]
        return MessageQuries.objects.filter(operator_id=operator_id, admin_id=self.request.user.id).order_by('-created_at')


class ClientInvoiceUpload(FormView):
    template_name = 'admin_invoice_upload.html'
    form_class = ClientInvoiceForm
    context_object_name = 'document'

    def post(self, request):
        form = ClientInvoiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Uploaded Successfully.")
            return HttpResponseRedirect(request.path_info)
        else:
            messages.error(request, "Failed to upload.")
            form = OperatorDocumentsForm()
            return HttpResponseRedirect(request.path_info)


class AdminInvoiceList(ListView):
    template_name = 'admin_invoice_list.html'
    model = Invoices
    context_object_name = 'documents'
    paginate_by = 10

    def get_queryset(self):
        return Invoices.objects.all().order_by('-created_at')


def invoiceDelete(request, pk):
    if request.user.is_staff:
        document = Invoices.objects.get(invoice_id=pk)
        if document:
            document.invoices.delete()
            document.delete()
            messages.success(request, "Deleted Successfully.")
            return HttpResponseRedirect(reverse('clientApp:admin_invoice_list'))
        else:
            messages.error(request, "Error while deleting the file.")
            return HttpResponseRedirect(request.path_info)


class ClientInvoiceList(ListView):
    template_name = 'client_invoice_view.html'
    model = Invoices
    context_object_name = 'documents'
    paginate_by = 10

    def get_queryset(self):
        Invoices.objects.filter(client_id=self.request.user.client.client_user_id,
                                read_by_client=False).update(read_by_client=True)
        return Invoices.objects.filter(client_id=self.request.user.client.client_user_id).order_by('-created_at')


class EmployeeDocumentsUpload(FormView):
    form_class = EmployeeDocumentsForm
    template_name = 'operator_documents_upload.html'
    success_url = reverse_lazy("clientApp:home")
    context_object_name = 'document'

    def post(self, request):
        form = EmployeeDocumentsForm(request.POST, request.FILES)
        files = request.FILES.getlist('documents')
        if form.is_valid():
            for doc in files:
                document = EmployeeDocuments(
                    employee_id=request.user.employee,
                    doc_title=doc.name,
                    documents=doc
                )
                document.save()
            messages.success(request, "Uploaded Successfully.")
            return HttpResponseRedirect(request.path_info)
        else:
            messages.error(request, "Failed to upload: Invalid files.")
            form = OperatorDocumentsForm()


class EmployeeDocumentsList(ListView):
    template_name = 'operator_documents_list.html'
    model = EmployeeDocuments
    context_object_name = 'documents'
    paginate_by = 10

    def get_queryset(self):
        return EmployeeDocuments.objects.filter(employee_id=self.request.user.employee.employee_user_id)


class EmployeeHolidayRequest(TemplateView):
    template_name = 'operator_leave_request.html'

    def get(self, request):
        form = EmployeeHolidayForm()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        context = {}
        if request.user.employee:
            form = EmployeeHolidayForm(request.POST)
            if form.is_valid():
                # Calculate no. of holidays
                day = form.cleaned_data['to_date'] - \
                    form.cleaned_data['from_date']
                total_days = day.days
                if(total_days > 0):
                    total_days = total_days + 1
                if(total_days == 0):
                    total_days = 1

                if(total_days >= 1):
                    admin = User.objects.get(is_staff=True, is_superuser=True)
                    data = form.save(commit=False)
                    data.no_of_days = total_days
                    data.employee_id = self.request.user.employee
                    data.admin_id = admin
                    data.save()
                    messages.success(
                        request, "Your holiday request has been submitted! We will get back in touch with you soon. Thank you")
                else:
                    messages.error(request, "Kindly select a valid date range")
                return HttpResponseRedirect(request.path_info)
            else:
                context['form'] = form()
                return render(request, self.template_name, context)
        else:
            return redirect('clientApp:home')


class EmployeeHolidayList(ListView):
    template_name = 'operator_leave_list.html'
    model = EmployeeHoliday
    context_object_name = 'leave_list'
    paginate_by = 10

    def get_queryset(self):
        action = self.request.path.split('/')[-1]
        if action == "Pending":
            EmployeeHoliday.objects.filter(employee_id=self.request.user.employee.employee_user_id,
                                           leave_status="Pending", read_by_employee=False).update(read_by_employee=True)
        return EmployeeHoliday.objects.filter(employee_id=self.request.user.employee.employee_user_id, leave_status=action).order_by('-created_at')


class EmployeeLeaveDetail(DetailView):
    model = EmployeeHoliday
    template_name = 'employee_holiday_detail.html'
    context_object_name = 'leave'


class AdminEmployeeFeedback(TemplateView):
    template_name = 'client_feedback.html'

    def get(self, request):
        feedback = EmployeeFeedbackForm()
        context = {
            'feedback': feedback
        }
        return render(request, self.template_name, context)

    def post(self, request):
        context = {}
        feedback_form = EmployeeFeedbackForm(request.POST)
        if feedback_form.is_valid():
            data = feedback_form.save(commit=False)
            data.admin_id = self.request.user
            data.save()
            messages.success(
                request, "Your feedback has been submitted. Thank you")
            return HttpResponseRedirect(request.path_info)
        else:
            context['feedback_form'] = feedback_form()
        return render(request, self.template_name, context)


class EmployeeFeedbackList(ListView):
    template_name = 'employee_feedback_list.html'
    model = EmployeeFeedback
    context_object_name = 'feedback_list'
    paginate_by = 10

    def get_queryset(self):
        EmployeeFeedback.objects.filter(employee_id=self.request.user.employee.employee_user_id,
                                        read_by_employee=False).update(read_by_employee=True)

        # for search feedback
        query = self.request.GET.get("q")
        if query:
            return EmployeeFeedback.objects.filter(employee_id=self.request.user.employee.employee_user_id, rating__icontains=query)

        return EmployeeFeedback.objects.filter(employee_id=self.request.user.employee.employee_user_id).order_by('-created_at')


class AdminFeedbackList(ListView):
    template_name = 'admin_employee_feedback_list.html'
    model = EmployeeFeedback
    context_object_name = 'feedback_list'
    paginate_by = 10

    def get_queryset(self):
        # for search feedback
        query = self.request.GET.get("q")
        if query:
            return EmployeeFeedback.objects.filter(rating__icontains=query)

        return EmployeeFeedback.objects.all().order_by('-created_at')


class AdminEmployeeHolidayList(ListView):
    template_name = 'admin_employee_leave_list.html'
    model = EmployeeHoliday
    context_object_name = 'leave_list'
    paginate_by = 10

    def get_queryset(self):
        action = self.request.path.split('/')[-1]
        if action == "Pending":
            EmployeeHoliday.objects.filter(leave_status="Pending",
                                           read_by_admin=False).update(read_by_admin=True)
        
        query = self.request.GET.get("q")
        if query:
            return EmployeeHoliday.objects.filter(leave_status=action,  employee_id__employee_name__icontains=query)

        return EmployeeHoliday.objects.filter(leave_status=action).order_by('-created_at')


def employee_holiday_reject(request, pk):
    if request.user.is_staff:
        leave = EmployeeHoliday.objects.get(leave_id=pk)
        leave.updated_at = timezone.now()
        leave.leave_status = "Decline"
        leave.save()
        messages.success(
            request, "Holiday request has been declined. Thank you.")

        # send an email
        subject, from_email, to = "Holiday request declined", settings.EMAIL_HOST_USER, leave.employee_id.user_name.email
        text_content = "Employee Holiday request has been declined."
        html_content = f"""<p>Hi {leave.employee_id.employee_name}, <br> 
            Your holiday request has been declined. <br> 
            Your holiday summary is as follow. <br> 
            From: {leave.from_date} <br> 
            To: {leave.to_date} <br>
            Total Holidays: {leave.no_of_days} <br>
            Reason: {leave.reason} <br>
            Leave final status: {leave.leave_status} <br> <br>
            You can login by visiting our website for more details: <a> https://urbancommunications.herokuapp.com/ </a> </p>"""
        msg = EmailMultiAlternatives(
            subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        messages.success(
            request, "Email send to employee successfully.")

        return redirect('clientApp:home')
    else:
        messages.success(
            request, "You don't have valid permission to decline holiday request.")
        return redirect('clientApp:home')


def employee_holiday_approve(request, pk):
    if request.user.is_staff:
        leave = EmployeeHoliday.objects.get(leave_id=pk)
        leave.updated_at = timezone.now()
        leave.leave_status = "Approve"
        # send an email
        subject, from_email, to = "Holiday request approved", settings.EMAIL_HOST_USER, leave.employee_id.user_name.email
        text_content = "Employee Holiday request has been approved."
        html_content = f"""<p>Hi {leave.employee_id.employee_name}, <br> 
                Your holiday request has been Approved. <br> 
                Your holiday summary is as follow. <br> 
                From: {leave.from_date} <br> 
                To: {leave.to_date} <br>
                Total Holidays: {leave.no_of_days} <br>
                Reason: {leave.reason} <br>
                Leave status: {leave.leave_status} <br> <br>
                You can login by visiting our website for more details: <a> https://urbancommunications.herokuapp.com/ </a> </p>
                """
        msg = EmailMultiAlternatives(
            subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        messages.success(
            request, "Email send to employee successfully.")
        leave.save()
        messages.success(
            request, "Holiday request has been approved. Thank you.")
        return redirect('clientApp:home')
    

