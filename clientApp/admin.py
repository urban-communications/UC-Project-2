from django.contrib import admin
from clientApp.models import Client, Operator, Leave, Feedback

# Register your models here.
admin.site.register(Client)
admin.site.register(Operator)
admin.site.register(Leave)
admin.site.register(Feedback)
