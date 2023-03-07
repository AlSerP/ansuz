from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import Group
from accounts.models import CustomUser
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.conf import settings


class UserLoginView (LoginView):
    template_name = 'users/login.html'
    form_class = CustomAuthenticationForm


class UserLogoutView (LogoutView):
    next_page = reverse_lazy('login')


class UserSignUpView (CreateView):
    template_name = 'users/signup.html'
    success_url = reverse_lazy('login')
    form_class = CustomUserCreationForm
    success_message = "Your profile was created successfully"


class GroupCreateView (PermissionRequiredMixin, CreateView):
    template_name = 'forms/task_creation.html'
    success_url = reverse_lazy('home')
    model = Group
    fields = '__all__'
    permission_required = 'users.moderate_users'


class LeadersView (ListView):
    model = CustomUser
    context_object_name = 'users'
    template_name = 'leaderboard.html'

    def get_queryset(self, **kwargs):
        return CustomUser.objects.order_by('-score')


def update_user_score(request, pk):
    user = CustomUser.objects.get(pk=pk)
    user.update_score()

    return redirect(reverse_lazy('home'))

def update_all_users_score(request):
    users = CustomUser.objects.all()
    for user in users:
        user.update_score()
    return redirect(reverse_lazy('home'))

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
