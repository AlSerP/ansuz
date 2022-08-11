from django.urls import path
from . import views


urlpatterns = [
    path('<int:pk>/upload', views.UploadSolutionView.as_view(), name="upload_solution"),
    path('', views.ThemeTasksView.as_view(), name="home"),
    path('<int:pk>/', views.TaskView.as_view(), name='task'),
    path('create/', views.TaskCreationView.as_view(), name='create_task'),
    path('<pk>/delete/', views.TaskDeleteView.as_view(), name='delete_task'),
    path('<pk>/update/', views.TaskUpdateView.as_view(), name='update_task'),
    path('create-theme/', views.ThemeCreationView.as_view(), name='create_theme'),
]
