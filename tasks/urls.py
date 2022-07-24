from django.urls import path
from . import views


urlpatterns = [
    path('<int:pk>/upload', views.UploadSolutionView.as_view(), name="upload_solution"),
    path('', views.ThemeTasksView.as_view(), name="home"),
    path('<int:pk>/', views.TaskView.as_view(), name='task'),
]
