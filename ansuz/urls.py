from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('user/', include('accounts.urls')),
    # path('user/', include('django.contrib.auth.urls')),
    path('task/', include('tasks.urls')),
    path('', RedirectView.as_view(url='task/')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
