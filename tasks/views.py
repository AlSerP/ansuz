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
        form.instance.task = Task.objects.get(pk=self.kwargs.get('pk'))
        form.instance.user = self.request.user
        solution = form.save()
        solution.save()
        solution.compile()
        return super().form_valid(form)


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

        context['tests'] = data_task
        if self.request.user.is_authenticated:
            context['solutions'] = task.get_solutions(self.request.user)
            context['best_solution'] = task.get_best_solution(self.request.user)

        context['tts'] = Task.objects.filter(theme=Task.objects.get(id=self.kwargs.get('pk')).theme.id)

        return context

# def compile_solution(request):
#     if request.method == "POST":
#         solution = request.POST.get("username")
