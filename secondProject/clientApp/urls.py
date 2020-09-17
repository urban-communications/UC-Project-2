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
    path('operator/profile/<slug:pk>/', views.OperatorProfileView.as_view(), name='operator_profile'),
    path('feedback/', views.FeedbackView.as_view(), name='client_feedback'),
    path('feedback/list/', views.ListClientFeedbackView.as_view(), name='client_feedback_list'),
    path('feedback/operator/list/', views.ListOperatorFeedbackView.as_view(), name='operator_feedback_list'),
    path('feedback/admin/list/', views.ListAdminFeedbackView.as_view(), name='admin_feedback_list'),
    path('operator/leave-request/', views.OperatorLeaveRequest.as_view(), name='operator_leave_request'),
    path('operator/leave-request/list', views.OperatorLeaveList.as_view(), name='operator_leave_list'),
    path('operator/leave-request/detail/<slug:pk>', views.OperatorLeaveDetail.as_view(), name='operator_leave_detail'),
    path('leave-request/list', views.ClientLeaveList.as_view(), name='leave_list'),
    path('leave-request/approve/<slug:pk>', views.leave_approve, name='leave_approve'),
    path('leave-request/reject/<slug:pk>', views.leave_reject, name='leave_reject'),
    path('leave-request/admin/list', views.AdminLeaveList.as_view(), name='admin_leave_list'),
    path('operator/documents/upload', views.OperatorDocumentsUpload.as_view(), name='operator_document_upload'),
    path('operator/documents/list', views.OperatorDocumentsList.as_view(), name='operator_document_list'),
    path('operator/documents/delete/<slug:pk>', views.operatorDocumetDelete, name='operator_document_delete')
]

app_name = 'clientApp'