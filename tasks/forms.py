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


class TextSolutionForm(forms.Form):
    FILE_TYPES = (
        ('py', 'Python 3.6'),
        ('cpp', 'G++ 12.2.0'),
        ('txt', 'Text'),
    )
    type = forms.ChoiceField(choices=FILE_TYPES)
    text = forms.CharField(label='Текст', max_length=6000, widget=forms.Textarea(attrs={"rows": "20", "cols": "20", "spellcheck": "false", "class": "code_area"}))


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'

    help_texts = {
        'tests': 'Данные, которые будут передаваться в программу.',
        'answers': 'Ожидаемый выход из программы.',
    }
