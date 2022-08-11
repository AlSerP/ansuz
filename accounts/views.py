from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse_lazy


class UserLogin (LoginView):
    template_name = 'users/user_login.html'


# TODO: Возможность выдачи групп пользователям
def make_moderator(request):
    pass


def make_admin(request):
    # if request.method == 'POST':
    #     user_id = request.POST.get('user_id')
    #     user = settings.AUTH_USER_MODEL.objects.get(pk=user_id)
    #     user.groups.add('admin')
    # return redirect(reverse_lazy('home'))
    pass
