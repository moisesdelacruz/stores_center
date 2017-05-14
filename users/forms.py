from django import forms
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import (UserCreationForm,
    UserChangeForm, PasswordChangeForm, SetPasswordForm)

class UserCreateForm(UserCreationForm):
    password1 = forms.CharField(label='password',
        widget=forms.PasswordInput(attrs={'class': 'validate'}))
    password2 = forms.CharField(label='password confirmation',
        widget=forms.PasswordInput(attrs={'class': 'validate'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)
        widgets = {
            'username': forms.TextInput(attrs={'class': 'validate'}),
            'first_name': forms.TextInput(attrs={'class': 'validate'}),
            'last_name': forms.TextInput(attrs={'class': 'validate'}),
            'email': forms.EmailInput(attrs={'class': 'validate'}),
        }


class UserUpdateForm(UserChangeForm):

    class Meta:
        model = User
        fields = (
            'password',
            'username',
            'first_name',
            'last_name',
            'email',)

        widgets = {
            'username': forms.TextInput(attrs={'class': 'validate'}),
            'first_name': forms.TextInput(attrs={'class': 'validate'}),
            'last_name': forms.TextInput(attrs={'class': 'validate'}),
            'email': forms.EmailInput(attrs={'class': 'validate'}),
        }

class PasswordUpdateForm(PasswordChangeForm):
    """
    A form that lets a user change their password by entering their old
    password.
    """
    error_messages = dict(SetPasswordForm.error_messages, **{
        'password_incorrect': _("Your old password was entered incorrectly. Please enter it again."),
    })
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autofocus': True, 'class': 'validate'}),
    )

    field_order = ['old_password', 'new_password1', 'new_password2']

    def clean_old_password(self):
        """
        Validate that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password
