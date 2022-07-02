from django.core.management.base import BaseCommand, CommandError
from appmigrations.fake_data import populate


class Command(BaseCommand):
    help = 'populates db with fake data'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):        
        populate()


