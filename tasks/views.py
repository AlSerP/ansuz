from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
from .models import Solution, Task, Theme
from django.contrib.auth.models import Permission
from django.urls import reverse_lazy
from django.shortcuts import redirect
from accounts.models import CustomUser
from django.contrib.contenttypes.models import ContentType
from accounts.forms import GroupSelectForm
from tasks.forms import SolutionUpdateForm
from django.contrib.auth.models import Group
from django.views.generic.edit import FormView
from django.conf import settings
import subprocess

def create_permission(per_code, per_name, con_type):
    tasks_per, created = Permission.objects.get_or_create(codename=per_code,
                                                          name=per_name,
                                                          content_type=con_type)
    return created


def get_theme_permission_code(theme):
    return f'view_theme{theme.pk}'


def get_permission_by_theme(theme: Theme):
    return Permission.objects.get(codename=f'view_theme{theme.pk}')


class UploadSolutionView(PermissionRequiredMixin, CreateView):
    """Отправка решения"""
    model = Solution
    template_name = 'solution.html'
    fields = ['upload']

    def has_permission(self,  **kwargs):
        user = self.request.user
        task = Task.objects.get(id=self.kwargs.get('pk'))
        return user.has_perm(f'view_theme{task.theme.id}')

    def form_valid(self, form):
        task = Task.objects.get(pk=self.kwargs.get('pk'))
        if task.is_open and task.is_visible:
            form.instance.task = task
            form.instance.user = self.request.user
            solution = form.save()
            solution.save()
            solution.compile()
            return super().form_valid(form)
        return redirect(reverse_lazy('home'))

    def get_success_url(self, **kwargs):
        return reverse_lazy('task', kwargs={'pk': self.kwargs.get('pk')})


class ThemeTasksView(LoginRequiredMixin, ListView):
    """Тема со всеми задачами"""
    model = Task
    context_object_name = 'themes'
    # context_object_name = 'themes'
    template_name = 'tasks/category.html'

    def get_queryset(self, **kwargs):
        allowed_themes = []
        for theme in Theme.objects.all():
            if self.request.user.has_perm(f'tasks.{get_theme_permission_code(theme)}'):
                allowed_themes.append(theme)

        return allowed_themes


class TaskView(PermissionRequiredMixin, DetailView):
    """Отдельная задача"""
    model = Task
    template_name = 'tasks/task_page.html'
    context_object_name = 'task'

    def has_permission(self,  **kwargs):
        user = self.request.user
        task = Task.objects.get(id=self.kwargs.get('pk'))
        return user.has_perm(f'view_theme{task.theme.id}')

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

        context['tests'] = data_task[:2]

        if self.request.user.is_authenticated:
            if self.kwargs.get('user') and self.request.user.has_perm('tasks.edit_tasks'):
                user = CustomUser.objects.get(username=self.kwargs.get('user'))
            else:
                user = self.request.user
            context['solutions'] = task.get_solutions(user).order_by('-id')
            context['best_solution'] = task.get_best_solution(user)

        context['theme_tasks'] = Task.objects.filter(theme=Task.objects.get(id=self.kwargs.get('pk')).theme.id)

        return context


class TaskCreationView(PermissionRequiredMixin, CreateView):
    """Создание задачи"""
    model = Task
    template_name = 'forms/task_creation.html'
    fields = '__all__'
    success_url = reverse_lazy('home')
    permission_required = 'tasks.edit_tasks'

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
    permission_required = 'tasks.edit_tasks'


class TaskUpdateView(PermissionRequiredMixin, UpdateView):
    model = Task
    fields = '__all__'
    template_name = 'forms/task_update.html'
    permission_required = 'tasks.edit_tasks'

    def get_success_url(self, **kwargs):
        return reverse_lazy('task', kwargs={'pk': self.kwargs.get('pk')})


class ThemeCreationView(PermissionRequiredMixin, CreateView):
    """Создание задачи"""
    model = Theme
    template_name = 'forms/task_creation.html'
    fields = '__all__'
    success_url = reverse_lazy('home')
    permission_required = 'tasks.edit_tasks'

    def form_valid(self, form):
        # form.instance.user = self.request.user
        # TODO: Сохранить создателя темы
        theme = form.save()
        theme.save()

        per_code = f'view_theme{theme.pk}'
        per_name = f'Can view Theme #{theme.pk}'
        theme_type = ContentType.objects.get(app_label='tasks', model='theme')
        print(per_code)
        print(create_permission(per_code, per_name, theme_type))

        return super().form_valid(form)


class TaskSolutionsView(PermissionRequiredMixin, ListView):
    model = Solution
    context_object_name = 'solutions'
    template_name = 'tasks/solutions_list.html'
    permission_required = 'tasks.edit_tasks'

    def get_queryset(self, **kwargs):
        task = Task.objects.get(id=self.kwargs.get('pk'))
        return Solution.objects.filter(task=task)


class SolutionFileView(LoginRequiredMixin, DetailView):
    model = Solution
    template_name = 'tasks/solution.html'
    context_object_name = 'solution'

    def get_context_data(self, **kwargs):
        context = super(SolutionFileView, self).get_context_data(**kwargs)
        print(context['solution'].upload)
        # sol = Solution.objects.all()
        # for s in sol:
        #     print(s.pk)
        #
        #f = open('./media/' + str(context['solution'].upload), 'r')
        f = open(settings.MEDIA_ROOT + '/' + str(context['solution'].upload), 'r')
        file_text = f.read()
        f.close()
        context['file_text'] = file_text
        # status = subprocess.run(["g++-7", "--version"])
        # status = subprocess.run(['bash','-c', 'ls /usr/bin/'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return context


class SolutionDeleteView(PermissionRequiredMixin, DeleteView):
    model = Solution
    success_url = reverse_lazy('home')
    template_name = 'forms/solution_delete.html'
    permission_required = 'tasks.edit_tasks'


class SolutionUpdateView(PermissionRequiredMixin, UpdateView):
    model = Solution
    success_url = reverse_lazy('home')
    form_class = SolutionUpdateForm
    template_name = 'forms/solution_update.html'
    permission_required = 'tasks.edit_tasks'

    def form_valid(self, form):
        self.object = form.save()
        self.object.user.update_score()
        return redirect(self.get_success_url())

    def get_success_url(self, **kwargs):
        return reverse_lazy('solution', kwargs={'pk': self.kwargs.get('pk')})


class ThemePermissionAppendView(PermissionRequiredMixin, FormView):
    template_name = 'forms/task_creation.html'
    permission_required = 'tasks.edit_tasks'
    form_class = GroupSelectForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        codename = f'view_theme{self.kwargs.get("pk")}'
        for group in form.cleaned_data['groups']:
            group.permissions.add(Permission.objects.get_or_create(codename=codename))

        return super().form_valid(form)


def get_groups_by_permission(permission: str):
    perm = Permission.objects.get(codename=permission)
    groups = Group.objects.all()
    res = []
    for group in groups:
        if perm in group.permissions.all():
            res.append(group)
    return res
