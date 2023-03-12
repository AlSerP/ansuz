from django import template
import json

register = template.Library()


@register.simple_tag(name='get_percents_by_solution')
def get_percents_by_solution(solution):
    return solution.mark * 100 // solution.task.score


@register.simple_tag(name='get_percents')
def get_percents(task, user):
    if task.get_best_solution(user):
        return task.get_best_solution(user).mark * 100 // task.score
    else:
        return '-'


@register.simple_tag(name='get_mark')
def get_mark(task, user):
    if task.get_best_solution(user):
        return task.get_best_solution(user).mark
    else:
        return '-'


@register.filter(name='str_to_json')
def str_to_json(string):
    if string:
        return json.loads(string)
    return None


@register.simple_tag(name='can_edit_tasks')
def can_edit_tasks(user):
    return user.has_perm('tasks.edit_tasks')


@register.simple_tag(name='get_file_name')
def get_file_name(upload):
    return str(upload).split('/')[-1]
