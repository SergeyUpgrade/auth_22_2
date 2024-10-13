from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, UserChangeForm
from django.forms import forms

from catalog.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

class ResetPasswordForm(StyleFormMixin, PasswordResetForm):
    """Форма для сброса пароля"""

    class Meta:
        model = User
        fields = ['email', ]
