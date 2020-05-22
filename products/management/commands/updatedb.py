from django.core.management.base import BaseCommand
from products.dbupdater import check_categories


class Command(BaseCommand):
    help = "database's weekly update"

    def handle(self, *args, **options):
        check_categories()
