from django.core.management.base import BaseCommand

from ...methods import check_and_add_pre_calculated_songs_to_db


# Thanks to https://adrienvanthong.medium.com/django-how-to-write-custom-admin-commands-f34522a3fcd1
class Command(BaseCommand):
    help = "Checks and adds pre-calculated songs to the database."

    def handle(self, *args, **options):
        check_and_add_pre_calculated_songs_to_db()
        self.stdout.write("Pre-calculated songs have been checked and added to the database.")
