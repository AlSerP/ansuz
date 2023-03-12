from django.urls import path
from . import views


urlpatterns = [
    path('', views.ThemeTasksView.as_view(), name="home"),
    path('create/', views.TaskCreationView.as_view(), name='create_task'),
    path('create-theme/', views.ThemeCreationView.as_view(), name='create_theme'),
    path('<int:pk>/', views.TaskView.as_view(), name='task'),
    path('<int:pk>/upload', views.UploadSolutionView.as_view(), name="upload_solution"),
    # path('<int:pk>/text-upload', views.UploadTextSolutionView.as_view(), name="upload_text_solution"),
    path('<pk>/delete/', views.TaskDeleteView.as_view(), name='delete_task'),
    path('<pk>/update/', views.TaskUpdateView.as_view(), name='update_task'),
    path('<pk>/solutions/', views.TaskSolutionsView.as_view(), name='task_solutions'),
    # path('<int:pk>/<user>', views.TaskView.as_view(), name='user_solutions'),
    path('solution/<int:pk>/', views.SolutionFileView.as_view(), name='solution'),
    path('solution/<int:pk>/update', views.SolutionUpdateView.as_view(), name='update_solution'),
    path('solution/<int:pk>/delete', views.SolutionDeleteView.as_view(), name='delete_solution'),
    path('perm/<pk>', views.ThemePermissionAppendView.as_view(), name='theme_permission'),
]
