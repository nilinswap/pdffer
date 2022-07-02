from django.core.management.base import BaseCommand
from pdffer.model_ops import test


class Command(BaseCommand):
    help = 'tests model_ops, the wrapper over db operations'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):        
        test()
