from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
from .models import Solution, Task, Theme
from django.urls import reverse_lazy


class UploadSolutionView(LoginRequiredMixin, CreateView):
    """Отправка решения"""
    model = Solution
    template_name = 'solution.html'
    fields = ['upload']

    def form_valid(self, form):
        form.instance.task = Task.objects.get(pk=self.kwargs.get('pk'))
        form.instance.user = self.request.user
        solution = form.save()
        solution.save()
        solution.compile()
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy('task', kwargs={'pk': self.kwargs.get('pk')})


class ThemeTasksView(ListView):
    """Тема со всеми задачами"""
    model = Task
    context_object_name = 'themes'
    # context_object_name = 'themes'
    template_name = 'tasks/category.html'

    def get_queryset(self, **kwargs):
        return Theme.objects.all()
        # return themes
        # if Tag.objects.filter(name=tag_name).exists():
        #     # return Image.objects.filter(tags__contains=self.request.GET['search'])
        #     return Tag.objects.get(name=tag_name).image_set.all()


class TaskView(DetailView):
    """Отдельная задача"""
    model = Task
    template_name = 'tasks/task_page.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super(TaskView, self).get_context_data(**kwargs)
        task = Task.objects.get(id=self.kwargs.get('pk'))

        tests = task.tests
        tests = tests[1:-1].replace('"', '').split(',')
        answers = task.answers
        answers = answers[1:-1].replace('"', '').split(',')

        data_task = []
        for test, answer in zip(tests, answers):
            data_task.append([test, answer])
        data_task.reverse()

        context['tests'] = data_task

        if self.request.user.is_authenticated:
            context['solutions'] = task.get_solutions(self.request.user)
            context['best_solution'] = task.get_best_solution(self.request.user)

        context['theme_tasks'] = Task.objects.filter(theme=Task.objects.get(id=self.kwargs.get('pk')).theme.id)

        return context


class TaskCreationView(PermissionRequiredMixin, CreateView):
    """Создание задачи"""
    model = Task
    template_name = 'forms/task_creation.html'
    fields = '__all__'
    success_url = reverse_lazy('home')
    permission_required = 'tasks.can_create_task'

    def form_valid(self, form):
        # form.instance.user = self.request.user
        # TODO: Сохранить создателя задачи
        task = form.save()
        task.save()
        return super().form_valid(form)


class TaskDeleteView(PermissionRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('home')
    template_name = 'forms/task_delete.html'
    permission_required = 'tasks.can_create_task'


class TaskUpdateView(PermissionRequiredMixin, UpdateView):
    model = Task
    fields = '__all__'
    template_name = 'forms/task_update.html'
    permission_required = 'tasks.can_create_task'

    def get_success_url(self, **kwargs):
        return reverse_lazy('task', kwargs={'pk': self.kwargs.get('pk')})
