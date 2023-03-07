from django.views.generic import TemplateView, ListView
from tasks.models import Task, Theme


class HomePageView(ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'tasks/category.html'

    def get_queryset(self, **kwargs):
        try:
            theme_id = Theme.objects.get(title="Тема 0")
        except Theme.DoesNotExist:
            theme_id = None

        return Task.objects.filter(theme=theme_id)

class YandexPageView(TemplateView):
    template_name = 'yandex.html'
