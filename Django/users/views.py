from django.contrib.auth.forms import password_validation as password_validation
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm as DefaultUserCreationForm
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView

from users.models import *


class UserCreationForm(DefaultUserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    error_messages = {
        'password_mismatch': _("Пароли не совпадают."),
    }

    first_name = forms.CharField(
        label=_("Имя"),
        widget=forms.TextInput,
        strip=True
    )
    last_name = forms.CharField(
        label=_("Фамилия"),
        widget=forms.TextInput,
        strip=True
    )
    email = forms.EmailField(
        label=_("E-Mail"),
        widget=forms.EmailInput
    )
    password1 = forms.CharField(
        label=_("Пароль"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Подтверждение пароля"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с данным E-mail уже существует!')
        return email


class Register(FormView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'

    def form_valid(self, form):
        username = form['username'].data

        form.save()
        user = User.objects.get(username=username)

        profile = Profile(user=user)
        profile.generate_tokens()
        profile.save()
        return super().form_valid(form)


@login_required
def profile(request):
    return render(request, 'profile.html')
