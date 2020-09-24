from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.edit import FormView
from clientApp.models import Operator, Feedback
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.contrib import messages


from clientApp.forms import FeedbackForm, LeaveForm, OperatorDocumentsForm

from clientApp.models import Client, Leave, OperatorDocuments


class HomeView(TemplateView):
    template_name = 'home.html'


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
        # operators = Operator.objects.filter(client_id=request.user.client)
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
                return redirect('clientApp:home')
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
    paginate_by = 5

    def get_queryset(self):
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
        constxt = {}
        if request.user.operator:
            form = LeaveForm(request.POST)
            if form.is_valid():
                data = form.save(commit=False)
                data.operator_id = self.request.user.operator
                data.client_id = self.request.user.operator.client_id
                data.save()
                return redirect('clientApp:home')
            else:
                context['form'] = form()
                return render(request, self.template_name, context)
        else:
            return redirect('clientApp:home')


class OperatorLeaveList(ListView):
    template_name = 'operator_leave_list.html'
    model = Leave
    context_object_name = 'leave_list'
    paginate_by = 5

    def get_queryset(self):
        return Leave.objects.filter(operator_id=self.request.user.operator.operator_user_id).order_by('-created_at')


class OperatorLeaveDetail(DetailView):
    model = Leave
    template_name = 'leave_detail.html'
    context_object_name = 'leave'


class ClientLeaveList(ListView):
    template_name = 'client_leave_list.html'
    model = Leave
    context_object_name = 'leave_list'
    paginate_by = 8

    def get_queryset(self):
        return Leave.objects.filter(client_id=self.request.user.client.client_user_id).order_by('-created_at')


def leave_approve(request, pk):
    if request.user.is_staff:
        leave = Leave.objects.get(leave_id=pk)
        leave.admin_leave_status = "Approved"
        leave.updated_at = timezone.now()
        if leave.client_leave_status == "Approved":
            leave.leave_status = "Approved"
        leave.save()
        return redirect("clientApp:home")
    elif hasattr(request.user, 'client'):
        leave = Leave.objects.get(leave_id=pk)
        leave.client_leave_status = "Approved"
        leave.updated_at = timezone.now()
        if leave.admin_leave_status == "Approved":
            leave.leave_status = "Approved"
        leave.save()
        return redirect("clientApp:home")
    else:
        return redirect("clientApp:home")


def leave_reject(request, pk):
    if request.user.is_staff or hasattr(request.user, 'client'):
        leave = Leave.objects.get(leave_id=pk)
        leave.updated_at = timezone.now()
        if hasattr(request.user, 'client'):
            leave.client_leave_status = "Declined"
        if request.user.is_staff:
            leave.admin_leave_status = "Declined"
        leave.leave_status = "Declined"
        leave.save()
        return redirect("clientApp:home")
    else:
        return redirect("clientApp:home")


class AdminLeaveList(ListView):
    template_name = 'client_leave_list.html'
    model = Leave
    context_object_name = 'leave_list'
    paginate_by = 8

    def get_queryset(self):
        return Leave.objects.all().order_by('-created_at')

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
                    operator_id = request.user.operator,
                    doc_title = doc.name,
                    documents = doc
                )
                document.save()
                messages.success(request, "Uploaded Successfully")
            return HttpResponseRedirect(request.path_info)
        else:
            messages.error(request, "Failed to upload: Invalid files")
            form = OperatorDocumentsForm()

class OperatorDocumentsList(ListView):
    template_name = 'operator_documents_list.html'
    model = OperatorDocuments
    context_object_name = 'documents'
    paginate_by = 10

    def get_queryset(self):
        return OperatorDocuments.objects.filter(operator_id=self.request.user.operator.operator_user_id)

def operatorDocumetDelete(request, pk):
    if request.user.operator:
        document = OperatorDocuments.objects.get(doc_id=pk)
        if document:
            document.documents.delete()
            document.delete()
            messages.success(request, "Deleted Successfully")
            return HttpResponseRedirect(reverse('clientApp:operator_document_list'))
        else:
            messages.error(request, "Error while deleting the file")
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