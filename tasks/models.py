from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from time import gmtime, strftime
from tester.tests_module import test_solution
import json

statuses = [
    ('SE', 'Отправлено на проверку'),
    ('IP', 'Проверяется'),
    ('CO', 'Проверено'),
    ('ER', 'Ошибка'),
]


def directory_path(instance, filename):
    upload_time = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
    return ('user_{0}/%s/{1}' % upload_time).format(instance.user.id, filename)


class Theme(models.Model):
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.title


class Task(models.Model):
    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, related_name='tasks', null=True)
    title = models.CharField(max_length=120, null=False)
    description = models.CharField(max_length=500, null=True)
    text = models.TextField(null=False)

    tests = models.TextField(null=False)  # Use JSON
    answers = models.TextField(null=False)  # Use JSON

    is_open = models.BooleanField(default=True)
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_solutions(self, user):
        return self.solutions.filter(user=user)

    def get_best_solution(self, user):
        solutions = self.get_solutions(user).order_by("-mark")
        if solutions:
            return solutions[0]

        return None


class Solution(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=False, related_name='solutions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    mark = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    status = models.CharField(max_length=30, default=statuses[0][0], choices=statuses)
    upload = models.FileField(upload_to=directory_path, validators=[FileExtensionValidator(allowed_extensions=['cpp', 'py'])])

    response = models.CharField(max_length=250, null=True)
    tests = models.TextField(null=True)

    def __str__(self):
        if self.status == statuses[2]:
            return f'{self.task} + {self.status} + {self.mark}'
        return f'{self.task} + {self.status}'

    def compile(self):
        compiled: dict = test_solution(str(self.upload), self.task.tests, self.task.answers)
        print(compiled['return_code'])
        self.status = compiled['return_code']
        if self.status != 'ER':
            self.response = str(compiled['tests_passed']) + '/' + str(compiled['tests_number'])
            self.mark = compiled['mark']
            self.tests = json.dumps(compiled['results'])
        else:
            self.response = compiled['message']
        # result = test_cpp(directory_path, self.task.tests, self.task.answers)


# myModel = MyModel()
# listIWantToStore = [1,2,3,4,5,'hello']
# myModel.myList = json.dumps(listIWantToStore)
# myModel.save()
