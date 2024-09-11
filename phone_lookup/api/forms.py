# api/forms.py

from django import forms
from .models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Phone Number", widget=forms.TextInput(attrs={'autofocus': True}))

    def clean(self):
        phone_number = self.cleaned_data.get('username')  # username is treated as phone_number
        password = self.cleaned_data.get('password')

        if phone_number and password:
            self.user_cache = authenticate(phone_number=phone_number, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['phone_number', 'name', 'email', 'password']

    # Ensure password validation is handled
    def clean_password(self):
        password = self.cleaned_data.get('password')
        # Add your password validation logic if necessary
        return password

class SpamReportForm(forms.Form):
    phone_number = forms.CharField(max_length=15, label="Phone Number to Report as Spam")