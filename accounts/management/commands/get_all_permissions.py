from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission


class Command(BaseCommand):
    help = 'Print all Permissions'

    def handle(self, *args, **options):
        permissions = Permission.objects.all()
        for perm in permissions:
            print(f'{perm.codename}  |  {perm.name}  |  {perm.content_type}')
