from django.core.management.base import BaseCommand

from ...methods import add_albums_and_songs


# Thanks to https://adrienvanthong.medium.com/django-how-to-write-custom-admin-commands-f34522a3fcd1
class Command(BaseCommand):
    help = """Adds songs from a folder, if there are subfolders, they are used as albums.
    Add album_art.jpg if you also want to add album art."""

    def handle(self, *args, **options):
        add_albums_and_songs()
        self.stdout.write("New albums and songs have been added to the database.")
