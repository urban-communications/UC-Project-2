from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView, ListView
from clientApp.models import Operator, Feedback

from clientApp.forms import FeedbackForm

from clientApp.models import Client


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
        if(request.user.client):
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
