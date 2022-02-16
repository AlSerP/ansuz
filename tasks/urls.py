from django.urls import path
from . import views


urlpatterns = [
    path('upload', views.UploadSolutionView.as_view(), name="upload_solution"),
    path('category', views.ThemeTasksView.as_view(), name="category_show"),
    path('<int:pk>/', views.TaskView.as_view(), name='task_show'),
]
