from django import template

register = template.Library()


@register.simple_tag(name='get_mark')
def get_mark(task, user):
    if task.get_best_solution(user):
        return task.get_best_solution(user).mark
    else:
        return '-'
