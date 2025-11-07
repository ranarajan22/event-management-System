from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Event, Registration

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'role']

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'name', 'organiser', 'sponsor', 'category', 'event_datetime',
            'one_line_description', 'complete_description', 'eligibility',
            'rewards', 'status', 'winner'
        ]
        widgets = {
            'event_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'status': forms.Select(),
        }

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        winner = cleaned_data.get('winner')

        if status == 'Completed' and not winner:
            self.add_error('winner', "Please specify the winner for completed events.")

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['full_name', 'email', 'date_of_birth', 'phone_number']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }