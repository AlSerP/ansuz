from django import forms
from .models import Solution, Task


class SolutionForm(forms.ModelForm):
    class Meta:
        model = Solution
        fields = ('upload',)


class SolutionUpdateForm(forms.ModelForm):
    class Meta:
        model = Solution
        fields = ('mark',)


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'

    help_texts = {
        'tests': 'Данные, которые будут передаваться в программу.',
        'answers': 'Ожидаемый выход из программы.',
    }
