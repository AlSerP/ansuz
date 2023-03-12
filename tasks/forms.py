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


class TextSolutionForm(forms.ModelForm):
    FILE_TYPES = (
        ('Py', 'Python 3.6'),
        ('C++', 'G++ 12.2.0'),
        ('TXT', 'Text'),
    )
    type = forms.ChoiceField(choices=FILE_TYPES)
    text = forms.CharField(label='Your name', max_length=100)


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'

    help_texts = {
        'tests': 'Данные, которые будут передаваться в программу.',
        'answers': 'Ожидаемый выход из программы.',
    }
