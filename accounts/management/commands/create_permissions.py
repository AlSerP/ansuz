from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from tasks.models import Task


# import logging

# GROUPS = ['student', 'moderator', 'admin']
# MODELS = ['solution']
# PERMISSIONS = ['send', ]  # For now only send permission by default for all, others include add, delete, change


def set_group_permissions(group_name, permissions):
    group, created = Group.objects.get_or_create(name=group_name)
    for permission in permissions:
        group.permissions.add(permission)


class Command(BaseCommand):
    help = 'Creates task creating permissions'

    def handle(self, *args, **options):
        task_type = ContentType.objects.get(app_label='tasks', model='task')
        user_type = ContentType.objects.get(app_label='accounts', model='customuser')
        solution_type = ContentType.objects.get(app_label='tasks', model='solution')

        tasks_per, created = Permission.objects.get_or_create(codename='edit_tasks',
                                                              name='Can create Task',
                                                              content_type=task_type)  # creating permissions

        user_per, created = Permission.objects.get_or_create(codename='moderate_users',
                                                             name='Can ban|block Users',
                                                             content_type=user_type)  # creating permissions

        solution_per, created = Permission.objects.get_or_create(codename='check_solutions',
                                                                 name='Can check Solutions',
                                                                 content_type=solution_type)  # creating permissions
        set_group_permissions('admin', (tasks_per, user_per, solution_per))
        set_group_permissions('moderator', (tasks_per, solution_per))

        self.stdout.write(self.style.SUCCESS('Default permissions created and applied'))
