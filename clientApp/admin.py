from django.contrib import admin
from clientApp.models import (
    Client, 
    Operator, 
    Leave, 
    Feedback, 
    MessageQuries,
    Invoices,
    Employee,
    EmployeeDocuments,
    EmployeeFeedback,
    EmployeeHoliday
)

admin.site.register(Client)
admin.site.register(Operator)
admin.site.register(Leave)
admin.site.register(Feedback)
admin.site.register(MessageQuries)
admin.site.register(Invoices)
admin.site.register(Employee)
admin.site.register(EmployeeDocuments)
admin.site.register(EmployeeFeedback)
admin.site.register(EmployeeHoliday)