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


class Employee(models.Model):
    employee_user_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    user_name = models.OneToOneField(User, on_delete=models.CASCADE)
    job_designation = models.CharField(max_length=100, null=False)
    employee_name = models.CharField(max_length=100, null=False)
    contact_number = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=200)
    total_leaves = models.IntegerField(null=False)
    available_leaves = models.IntegerField(null=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    profile_picture = models.ImageField(
        upload_to='employee_profile_picture', blank=True, null=True)

    def __str__(self):
        return self.employee_name


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
    read_by_operator = models.BooleanField(default=False)
    read_by_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.feedback_note


class Leave(models.Model):
    LEAVE_STATUS = (
        ('Pending', 'Pending'),
        ('Approve', 'Approve'),
        ('Decline', 'Decline')
    )
    leave_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    operator_id = models.ForeignKey(Operator, on_delete=models.CASCADE)
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    from_date = models.DateField(null=False)
    to_date = models.DateField(null=False)
    no_of_days = models.IntegerField(null=False)
    reason = models.TextField(null=True)
    leave_status = models.CharField(
        max_length=20, choices=LEAVE_STATUS, default='Pending')
    client_leave_status = models.CharField(max_length=20, default='Pending')
    admin_leave_status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True)
    read_by_operator = models.BooleanField(default=False)
    read_by_client = models.BooleanField(default=False)
    read_by_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.operator_id


class MessageQuries(models.Model):
    message_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    admin_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    operator_id = models.ForeignKey(
        Operator, on_delete=models.CASCADE, null=True)
    messageQuery = models.TextField(null=False)
    created_at = models.DateTimeField(default=timezone.now)
    sender = models.CharField(max_length=20, null=True)
    read_by_operator = models.BooleanField(default=False)
    read_by_client = models.BooleanField(default=False)
    read_by_admin = models.BooleanField(default=False)


class Invoices(models.Model):
    invoice_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=50, null=True)
    invoices = models.FileField(upload_to="client_invoices", null=False)
    read_by_client = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class EmployeeDocuments(models.Model):
    doc_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    doc_title = models.CharField(max_length=100, null=False)
    documents = models.FileField(upload_to="employee_documents", null=False)

    def __str__(self):
        return self.doc_title


class EmployeeHoliday(models.Model):
    LEAVE_STATUS = (
        ('Pending', 'Pending'),
        ('Approve', 'Approve'),
        ('Decline', 'Decline')
    )
    leave_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    admin_id = models.ForeignKey(User, on_delete=models.CASCADE)
    from_date = models.DateField(null=False)
    to_date = models.DateField(null=False)
    no_of_days = models.IntegerField(null=False)
    reason = models.TextField(null=True)
    leave_status = models.CharField(
        max_length=11, choices=LEAVE_STATUS, default='Pending')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True)
    read_by_employee = models.BooleanField(default=False)
    read_by_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.employee_id

class EmployeeFeedback(models.Model):
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
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    admin_id = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(default=timezone.now)
    rating = models.CharField(max_length=20, choices=RATING_CHOICES)
    feedback_note = models.TextField(null=False)
    read_by_employee = models.BooleanField(default=False)

    def __str__(self):
        return self.feedback_note
