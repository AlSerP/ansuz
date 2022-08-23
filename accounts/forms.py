from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser
from django.contrib.auth.models import Group


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'line-input', 'autocomplete': 'off', 'placeholder': 'Имя пользователя'}
        )
        self.fields['password1'].widget.attrs.update(
            {'class': 'line-input', 'placeholder': 'Пароль', 'onChange': 'checkPasswordMatch();'}
        )
        self.fields['password2'].widget.attrs.update(
            {'class': 'line-input', 'placeholder': 'Повторить пароль', 'onChange': 'checkPasswordMatch();'}
        )


class CustomAuthenticationForm(AuthenticationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'line-input', 'autocomplete': 'off', 'placeholder': 'Имя пользователя'}
        )
        self.fields['password'].widget.attrs.update(
            {'class': 'line-input', 'placeholder': 'Пароль'}
        )


class CustomUserChangeFrom(forms.ModelForm):

    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name')


class GroupSelectForm(forms.Form):
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all())
