from django.shortcuts import render
from django.contrib.auth.views import LoginView


class UserLogin (LoginView):
    template_name = 'users/user_login.html'


def make_moderator():
    pass


def make_admin():
    pass
