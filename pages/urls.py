from django.urls import path
from . import views
from django.views.generic.base import RedirectView


urlpatterns = [
    path('yandex_1f13969a9b869259.html', views.YandexPageView.as_view(), name="yandex"),
    path('', RedirectView.as_view(url='task/')),
]
