from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
import uuid


class Client(models.Model):
    CLIENT_TYPE = (
        ('', 'Choose...'),
        ('Taxi Firm', 'Taxi Firm'),
        ('Insurance Firm', 'Insurance Firm'),
        ('Others', 'Others')
    )
    client_user_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    user_name = models.OneToOneField(User, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=100, null=False)
    client_type = models.CharField(max_length=30, choices=CLIENT_TYPE)
    contact_number = models.CharField(max_length=30)
    address = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    profile_picture = models.ImageField(
        upload_to='client_profile_picture', blank=True, null=True)

    def __str__(self):
        return self.client_name


class Operator(models.Model):
    operator_user_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    user_name = models.OneToOneField(User, on_delete=models.CASCADE)
    client_id = models.ForeignKey(Client, null=True, on_delete=models.SET_NULL)
    operator_name = models.CharField(max_length=100, null=False)
    contact_number = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=200)
    total_leaves = models.IntegerField(null=False)
    available_leaves = models.IntegerField(null=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    profile_picture = models.ImageField(
        upload_to='operator_profile_picture', blank=True, null=True)

    def __str__(self):
        return self.operator_name


class OperatorDocuments(models.Model):
    doc_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    operator_id = models.ForeignKey(Operator, on_delete=models.CASCADE)
    doc_title = models.CharField(max_length=100, null=False)
    documents = models.FileField(upload_to="operator_documents", null=False)

    def __str__(self):
        return self.doc_title


class Feedback(models.Model):
    RATING_CHOICES = (
        ('', 'Choose...'),
        ('One Star', 'One Star'),
        ('Two Star', 'Two Star'),
        ('Three Star', 'Three Star'),
        ('Four Star', 'Four Star'),
        ('Five Star', 'Five Star'),
    )
    feedback_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    operator_id = models.ForeignKey(Operator, on_delete=models.CASCADE)
    client_id = models.ForeignKey(Client, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(default=timezone.now)
    rating = models.CharField(max_length=20, choices=RATING_CHOICES)
    feedback_note = models.TextField(null=False)

    def __str__(self):
        return self.feedback_note


class Leave(models.Model):
    LEAVE_STATUS = (
        ('Pending', 'Pending'),
        ('Approve', 'Approve'),
        ('Decline', 'Decline')
    )
    DAYS = (
        ('', 'Choose...'),
        ('One', 'One'),
        ('Two', 'Two'),
        ('Three', 'Three'),
        ('Four', 'Four'),
        ('Five', 'Five'),
        ('More', 'More')
    )
    leave_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    operator_id = models.ForeignKey(Operator, on_delete=models.CASCADE)
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    from_date = models.DateField(null=False)
    to_date = models.DateField(null=False)
    no_of_days = models.CharField(max_length=20, choices=DAYS)
    reason = models.TextField(null=True)
    leave_status = models.CharField(
        max_length=20, choices=LEAVE_STATUS, default='Pending')
    client_leave_status = models.CharField(max_length=20, default='Pending')
    admin_leave_status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True)

