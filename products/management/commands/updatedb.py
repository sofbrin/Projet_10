from django.core.management.base import BaseCommand
from products.dbupdater import ProductUpdater


class Command(BaseCommand):
    help = "database's weekly update"

    def add_arguments(self, parser):
        parser.add_argument('n_products', type=int, default=100, nargs='?')

    def handle(self, *args, **options):
        updater = ProductUpdater()
        updater.check_products(options['n_products'])
