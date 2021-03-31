import subprocess
from django.core.management.base import BaseCommand, CommandError

from ...models import Category
from django.contrib.auth.models import User, Group, Permission
from django.contrib.sites.models import Site


class Command(BaseCommand):
    help = 'Deploy base site with default database'


    def handle(self, *args, **options):

        subprocess.call(['python', './manage.py', 'collectstatic'])

        subprocess.call(['python', './manage.py', 'makemigrations'])
        subprocess.call(['python', './manage.py', 'migrate'])

        self.create_superuser()
        self.set_sites()
        self.create_categories()
        self.create_groups()
        self.set_superuser_group()
        self.set_permissions()


    def create_superuser(self):
        superuser = User.objects.filter(is_superuser=True)
        if superuser.exists():
            self.stdout.write('Superuser "%s" already exists' % superuser.get().username)
            return

        subprocess.call(['python', './manage.py', 'createsuperuser'])

    def create_groups(self):
        groups = [
            {'name': 'Адміністратори'},
            {'name': 'Модератори'},
            {'name': 'Користувачі з доступом'},
            {'name': 'Користувачі'}
        ]

        for args in groups:
            if not Group.objects.filter(name=args['name']).exists():
                group = Group.objects.create(name=args['name'])
                group.save()

                self.stdout.write('Successfully created group "%s"' % group.name)
            else:
                self.stdout.write('Group "%s" already exists' % args['name'])

    def create_categories(self):
        categories = [
            {
                'name': 'Робота сайту',
                'route': 'bugs',
            },
            {
                'name': 'Фотографії',
                'route': 'photo',
            },
            {
                'name': 'Новини',
                'route': 'news',
            },
            {
                'name': 'Спілкування',
                'route': 'board',
            },
            {
                'name': 'Події',
                'route': 'events',
            },
            {
                'name': 'Творчість',
                'route': 'сreative',
            },
            {
                'name': 'Спорядження',
                'route': 'equip',
            },
            {
                'name': 'Звіти',
                'route': 'reports',
            },
        ]

        for args in categories:
            if not Category.objects.filter(name=args['name']).exists():
                category = Category.objects.create(
                    name=args['name'],
                    route=args['route'],
                )
                category.publish()
                category.save()

                self.stdout.write('Successfully created category "%s"' % category.name)
            else:
                self.stdout.write('CmsCategory "%s" already exists' % args['name'])

    def set_superuser_group(self):
        superusers = User.objects.filter(is_superuser=True)
        admin_group = Group.objects.get(name='Адміністратори')
        for user in superusers:
            admin_group.user_set.add(user)
            self.stdout.write('User "%s" added to group "%s"' % (user, admin_group.name))

    def set_permissions(self):
        permissions = {
            'Адміністратори': [
                'add_user',
                'change_user',
                'delete_user',
                'add_group',
                'change_group',
                'delete_group',
                'add_tag',
                'change_tag',
                'delete_tag',
                'add_taggeditem',
                'change_taggeditem',
                'delete_taggeditem',
                'add_comment',
                'change_comment',
                'delete_comment',
                'moderate_comment',
                'add_post',
                'change_post',
                'delete_post',
                'moderate_post',
                'add_map',
                'change_map',
                'delete_map',
                'moderate_map',
                'add_category',
                'change_category',
                'delete_category',
                'hidden_access',
            ],
            "Модератори": [
                'change_user',
                'add_tag',
                'change_tag',
                'delete_tag',
                'add_taggeditem',
                'change_taggeditem',
                'delete_taggeditem',
                'add_comment',
                'change_comment',
                'delete_comment',
                'moderate_comment',
                'add_post',
                'change_post',
                'delete_post',
                'moderate_post',
                'add_map',
                'change_map',
                'delete_map',
                'moderate_map',
                'hidden_access',
            ],
            "Користувачі з доступом": [
                'add_comment',
                'change_comment',
                'delete_comment',
                'add_post',
                'change_post',
                'delete_post',
                'add_map',
                'change_map',
                'delete_map',
                'hidden_access',
            ],
            "Користувачі": [
                'add_comment',
                'change_comment',
                'delete_comment',
                'add_post',
                'change_post',
                'delete_post',
            ]
        }

        groups = Group.objects.all()

        for group in groups:
            if group.name in permissions:
                for perm in permissions[group.name]:
                    permission = Permission.objects.get(codename=perm)
                    group.permissions.add(permission)
                    self.stdout.write('Successfully added permission "%s" for group "%s"' % (permission.codename, group.name,))
            else:
                raise CommandError('No permissions for group "%s"' % group.name)

    def set_sites(self):
        site = Site.objects.get(id=1)
        site.name = 'diggers.kiev.ua'
        site.domain = 'diggers.kiev.ua'
        site.save()

        self.stdout.write('Successfully setup site "%s" with domain "%s"' % (site.name, site.domain,))


