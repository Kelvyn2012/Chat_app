from django.core.management.base import BaseCommand
from chat.models import Room


class Command(BaseCommand):
    help = "Seeds the database with initial data"

    def handle(self, *args, **options):
        rooms = [
            {"name": "General", "slug": "general"},
            {"name": "Technology", "slug": "technology"},
            {"name": "Sports", "slug": "sports"},
            {"name": "Music", "slug": "music"},
        ]

        for room in rooms:
            Room.objects.get_or_create(name=room["name"], slug=room["slug"])

        self.stdout.write(self.style.SUCCESS("Successfully seeded database"))
