import psycopg2
from django.core.management.base import BaseCommand
from ...models import Post, Map, Category, Comment, User


class Command(BaseCommand):
    help = 'Migrate from db old to db actiual'

    def handle(self, *args, **options):
        conn = psycopg2.connect(dbname='diggers_old', user='ramenky',
                                password='Sonata-Kova', host='localhost')
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Add users

        cursor.execute('SELECT * FROM auth_user '
                       'LEFT JOIN cms_cmsprofile '
                       'ON auth_user.id = cms_cmsprofile.user_id '
                       'where true')
        results = cursor.fetchall()
        for old_user in results:
            existing_user = User.objects.filter(username=old_user['username']).count()

            if existing_user:
                continue

            new_user = User.objects.create(
                username=old_user['username'],
                password=old_user['password'],
                last_login=old_user['last_login'],
                is_superuser=old_user['is_superuser'],
                first_name=old_user['first_name'],
                last_name=old_user['last_name'],
                email=old_user['email'],
                is_staff=old_user['is_staff'],
                is_active=old_user['is_active'],
                date_joined=old_user['date_joined'],
                avatar=old_user['avatar'],
                birth_date=old_user['birth_date'],
                is_banned=old_user['is_banned'],
                location=old_user['location'],
                last_activity=old_user['last_activity'],
                email_verified=old_user['email_verified'],
            )
            print('Created user %s' % new_user.username)

        # Add posts

        cursor.execute('SELECT * FROM cms_cmspost WHERE TRUE')
        posts = cursor.fetchall()

        categories = [
            'news',
            'creative',
            'reports',
            'events',
            'treads',
            'equip',
            'photo',
            'bugs',
        ]

        for value in categories:
            existing_category = Category.objects.filter(route=value).count()

            if existing_category:
                continue

            Category.objects.create(
                name=value,
                route=value,
            )

        for old_post in posts:
            existing_post = Post.objects.filter(title=old_post['title']).count()

            if existing_post:
                continue

            cursor.execute('SELECT username FROM auth_user WHERE id = %d' % old_post['author_id'])
            old_user = cursor.fetchone()
            author = User.objects.get(username=old_user['username'])

            category = Category.objects.get(route=categories[old_post['category_id'] - 1])

            cursor.execute('SELECT '
                           'taggit_tag.name '
                           'FROM taggit_taggeditem '
                           'LEFT JOIN taggit_tag ON taggit_taggeditem.tag_id=taggit_tag.id '
                           'WHERE taggit_taggeditem.object_id=%d' % old_post['id'])
            tags = cursor.fetchall()

            new_post = Post.objects.create(
                title=old_post['title'],
                author=author,
                category=category,
                created_date=old_post['created_date'],
                is_hidden=old_post['is_permited'],
                text=old_post['text'],
            )

            for tag in tags:
                new_post.tags.add(tag['name'])

            print('Post %s added to category %s' % (old_post['title'], category.name,))

        # Add maps

        cursor.execute('SELECT * FROM cms_map WHERE TRUE')
        maps = cursor.fetchall()

        for old_map in maps:
            existing_map = Map.objects.filter(title=old_map['title']).count()

            if existing_map:
                continue

            cursor.execute('SELECT username FROM auth_user WHERE id = %d' % old_map['author_id'])
            old_user = cursor.fetchone()
            author = User.objects.get(username=old_user['username'])

            cursor.execute('SELECT '
                           'taggit_tag.name '
                           'FROM taggit_taggeditem '
                           'LEFT JOIN taggit_tag ON taggit_taggeditem.tag_id=taggit_tag.id '
                           'WHERE taggit_taggeditem.object_id=%d' % old_map['id'])
            tags = cursor.fetchall()

            new_nap = Map.objects.create(
                title=old_map['title'],
                file=old_map['file'],
                description=old_map['description'],
                created_date=old_map['created_date'],
                author=author,
            )

            for tag in tags:
                new_nap.tags.add(tag['name'])

            print('Map %s added' % (old_map['title'],))

        # Add comments

        cursor.execute('SELECT * FROM cms_comment WHERE TRUE ORDER BY id ASC')
        comments = cursor.fetchall()

        for comment in comments:
            existing_comment = Comment.objects.filter(text=comment['text'])
            if existing_comment:
                continue

            cursor.execute('SELECT title FROM cms_cmspost WHERE id = %d' % comment['post_id'])
            original_post = cursor.fetchone()

            post = Post.objects.get(title=original_post['title'])

            cursor.execute('SELECT username FROM auth_user WHERE id = %d' % comment['author_id'])
            old_user = cursor.fetchone()
            author = User.objects.get(username=old_user['username'])

            parent = None
            if comment['parent_id']:
                cursor.execute('SELECT text FROM cms_comment WHERE id = %d' % comment['parent_id'])
                original_parent = cursor.fetchone()
                parent = Comment.objects.get(text=original_parent['text'])

            Comment.objects.create(
                text=comment['text'],
                is_deleted=comment['is_deleted'],
                created_date=comment['created_date'],
                author=author,
                parent=parent,
                post=post,
            )
            print('Created comment from %s' % author)

        cursor.close()
        conn.close()