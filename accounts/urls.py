from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name="login"),
    path('logout/', views.UserLogoutView.as_view(), name="logout"),
    path('signup/', views.UserSignUpView.as_view(), name="signup"),
    path('group/create/', views.GroupCreateView.as_view(), name="create_group"),
]

