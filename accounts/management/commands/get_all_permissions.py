from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission


class Command(BaseCommand):
    help = 'Print all Permissions'

    def handle(self, *args, **options):
        print(Permission.objects.all())