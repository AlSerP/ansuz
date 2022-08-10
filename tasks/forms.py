from django import forms
from .models import Solution, Task


class SolutionForm(forms.ModelForm):
    class Meta:
        model = Solution
        fields = ('upload',)


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'

    help_texts = {
        'tests': _('Данные, которые будут передаваться в программу.'),
        'answers': _('Ожидаемый выход из программы.'),
    }