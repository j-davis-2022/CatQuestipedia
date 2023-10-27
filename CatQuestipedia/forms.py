# from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Users
from django import forms
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError

class create_account_form(UserCreationForm):
    email = forms.EmailField(help_text=mark_safe("<ul><li>Your email is <span class='important'>not</span> required.</li><li>The only reason to input your email is to ensure it's you trying to change your password.</li><li>No emails will be sent to you, except in the case of a data breach.</li></ul>"), required=False)

    def clean_email(self):
        email = self.cleaned_data['email']
        if email != "":
            if Users.objects.filter(email=email).exists():
                raise ValidationError("That email is already used by another user.")
            else:
                return email

    class Meta:
        model = Users
        help_texts = {'username': '150 characters or fewer. Letters, digits and @/./+/-/_ only.'}
        fields = ["email", "username", "password1", "password2"]
