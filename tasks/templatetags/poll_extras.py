from django import template
import json

register = template.Library()


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
