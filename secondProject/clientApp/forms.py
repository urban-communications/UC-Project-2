from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from clientApp.models import Client, Operator, Feedback, Leave

CLIENT_TYPE = (
    ('', 'Choose...'),
    ('Taxi Firm', 'Taxi Firm'),
    ('Insurance Firm', 'Insurance Firm'),
    ('Others', 'Others')
)
RATING_CHOICES = (
    ('', 'Choose...'),
    ('One Star', 'One Star'),
    ('Two Star', 'Two Star'),
    ('Three Star', 'Three Star'),
    ('Four Star', 'Four Star'),
    ('Five Star', 'Five Star'),
)


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
    )
    first_name = forms.CharField(
        required=True,
    )
    last_name = forms.CharField(
        required=True,
    )
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'style': 'text-transform:lowercase;'})
    )

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )


class ClientRegistrationForm(forms.ModelForm):
    address = forms.CharField(
        max_length=150,
        required=True,
        label="Address",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter complete address'
        }),
    )
    contact_number = forms.CharField(
        required=True,
        label="Contact Number",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter contact number'
        }),
    )
    client_type = forms.ChoiceField(
        required=True,
        label="Client Type",
        choices=CLIENT_TYPE,
    )

    class Meta:
        model = Client
        fields = (
            'client_type',
            'contact_number',
            'address',
            'profile_picture'
        )


class OperatorRegistrationForm(forms.ModelForm):
    address = forms.CharField(
        max_length=150,
        required=True,
        label="Address",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter complete address'
        }),
    )
    contact_number = forms.CharField(
        required=True,
        label="Contact Number",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter contact number'
        }),
    )

    class Meta:
        model = Operator
        fields = (
            'client_id',
            'contact_number',
            'date_of_birth',
            'address',
            'total_leaves',
            'profile_picture'
        )


class FeedbackForm(forms.ModelForm):
    rating = forms.ChoiceField(
        required=True,
        label="Rating",
        choices=RATING_CHOICES
    )

    def __init__(self, request,  *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.fields['operator_id'].queryset = Operator.objects.filter(client_id=request.user.client.client_user_id)

    class Meta:
        model = Feedback
        fields = (
            'operator_id',
            'rating',
            'feedback_note'
        )


class LeaveForm(forms.ModelForm):

    class Meta:
        model = Leave
        fields = (
            'from_date',
            'to_date',
            'no_of_days'
        )
