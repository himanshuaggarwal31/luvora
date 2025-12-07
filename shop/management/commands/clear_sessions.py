"""
Management command to clear all Django sessions
Useful for clearing old sessions with incompatible data formats
"""
from django.core.management.base import BaseCommand
from django.contrib.sessions.models import Session


class Command(BaseCommand):
    help = 'Clear all Django sessions from database'

    def handle(self, *args, **options):
        count = Session.objects.count()
        Session.objects.all().delete()
        self.stdout.write(
            self.style.SUCCESS(f'Successfully cleared {count} session(s)')
        )
