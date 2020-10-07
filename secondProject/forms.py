from django import forms
from django.contrib.auth.forms import AuthenticationForm


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'autofocus': True ,'style': 'text-transform:lowercase;'})
    )

