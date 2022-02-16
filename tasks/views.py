from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DetailView
from .models import Solution, Task, Theme
from django.urls import reverse_lazy


class UploadSolutionView(LoginRequiredMixin, CreateView):
    """Отправка решения"""
    model = Solution
    template_name = 'solution.html'
    fields = ['upload']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.task = Task.objects.get(pk=1)
        form.instance.user = self.request.user
        solution = form.save()
        solution.save()
        return super().form_valid(form)


class ThemeTasksView(ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'tasks/category.html'

    def get_queryset(self, **kwargs):
        theme_id = Theme.objects.get(title="Тема 0")
        return Task.objects.filter(theme=theme_id)
        # if Tag.objects.filter(name=tag_name).exists():
        #     # return Image.objects.filter(tags__contains=self.request.GET['search'])
        #     return Tag.objects.get(name=tag_name).image_set.all()


class TaskView(DetailView):
    model = Task
    template_name = 'tasks/task_page.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super(TaskView, self).get_context_data(**kwargs)
        tests = Task.objects.get(id=self.kwargs.get('pk')).tests
        answers = Task.objects.get(id=self.kwargs.get('pk')).answers
        tests = tests[1:-1].replace("'", '').split(',')
        answers = answers[1:-1].replace("'", '').split(',')
        data_task = []
        for test, answer in zip(tests, answers):
            data_task.append([test, answer])
        print(data_task)
        context['tests'] = data_task

        context['tts'] = Task.objects.filter(theme=Task.objects.get(id=self.kwargs.get('pk')).theme.id)

        return context
