from django.contrib import admin
from clientApp.models import (
    Client, 
    Operator, 
    Leave, 
    Feedback, 
    MessageQuries,
    Invoices
)

admin.site.register(Client)
admin.site.register(Operator)
admin.site.register(Leave)
admin.site.register(Feedback)
admin.site.register(MessageQuries)
admin.site.register(Invoices)
