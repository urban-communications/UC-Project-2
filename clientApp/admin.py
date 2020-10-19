from django.contrib import admin
from clientApp.models import (
    Client, 
    Operator, 
    Leave, 
    Feedback, 
    MessageQuery,
    Invoice,
    Employee,
    OperatorDocument,
    EmployeeDocument,
    EmployeeFeedback,
    EmployeeHoliday
)

admin.site.register(Client)
admin.site.register(Operator)
admin.site.register(Leave)
admin.site.register(Feedback)
admin.site.register(MessageQuery)
admin.site.register(Invoice)
admin.site.register(Employee)
admin.site.register(EmployeeDocument)
admin.site.register(EmployeeFeedback)
admin.site.register(EmployeeHoliday)
admin.site.register(OperatorDocument)