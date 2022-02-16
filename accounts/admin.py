from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .forms import CustomUserChangeFrom, CustomUserCreationForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeFrom
    list_display = ['email', 'username', 'score']
    model = CustomUser


admin.site.register(CustomUser, CustomUserAdmin)
