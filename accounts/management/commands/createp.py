from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from tasks.models import Task
# import logging

# GROUPS = ['student', 'moderator', 'admin']
# MODELS = ['solution']
# PERMISSIONS = ['send', ]  # For now only send permission by default for all, others include add, delete, change


class Command(BaseCommand):
    help = 'Creates task creating permissions'

    def handle(self, *args, **options):
        group_name = 'moderator'
        app = 'tasks'
        model = 'task'
        content_type = ContentType.objects.get(app_label='tasks', model='task')
        permission, created = Permission.objects.get_or_create(codename='edit_tasks',
                                                               name='Can create Task',
                                                               content_type=content_type)  # creating permissions

        group, created = Group.objects.get_or_create(name=group_name)
        group.permissions.add(permission)

        # self.stdout.write(self.style.SUCCESS('Successfully created permission "%s"' % permission.name))
