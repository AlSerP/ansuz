from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm


class UserLoginView (LoginView):
    template_name = 'users/login.html'


class UserLogoutView (LogoutView):
    next_page = reverse_lazy('login')


class UserSignUpView (CreateView):
    template_name = 'users/signup.html'
    success_url = reverse_lazy('login')
    form_class = CustomUserCreationForm
    success_message = "Your profile was created successfully"


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
