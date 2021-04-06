import os
from django.conf import settings
from django.core.management.base import BaseCommand
from ...models import User


class Command(BaseCommand):
    help = 'Clear old unused avatars'

    def handle(self, *args, **options):
        avatars = []
        users = User.objects.all()
        for user in users:
            if not user.avatar:
                continue

            avatars.append(user.avatar.name.split('/')[1])

        avatars_root = os.path.join(settings.MEDIA_ROOT, 'avatars')

        for filename in os.listdir(avatars_root):
            if filename in avatars:
                continue
            os.remove(os.path.join(avatars_root, filename))
