from django.contrib import admin, messages
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter
from django.contrib.auth.admin import UserAdmin
from .models import User, Post, Comment, Category, PostAbstract, Map
from mptt.admin import MPTTModelAdmin


# Register your models here.


def send_activation(request, queryset):
    for user in queryset:
        pass

    messages.add_message(request, messages.INFO, 'Код підтвердження надіслано обраним користувачам')


send_activation.short_description = 'Надіслати код підтвердження'


@admin.register(User)
class DiggersUserAdmin(UserAdmin):
    list_filter = ['is_active', 'is_staff', 'email_verified', 'is_banned', 'last_login', 'date_joined']
    date_hierarchy = 'date_joined'
    list_display = (
        'username',
        'email',
        'is_active',
        'email_verified',
        'is_banned',
        'is_staff',
        'last_login',
        'date_joined'
    )
    fieldsets = UserAdmin.fieldsets + (('Profile', {'fields': ('avatar', 'email_verified', 'is_banned')}),)
    search_fields = ['username', 'email', 'first_name', 'last_name']
    actions = [send_activation]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    base_model = Category
    list_display = ('name', 'route')
    ordering = ('name', 'route')


@admin.register(Post)
class PostAdmin(PolymorphicChildModelAdmin):
    show_in_index = True

    list_filter = ('created_date', 'tags', 'is_hidden')
    list_display = ('title', 'created_date', 'modified_date', 'author', 'is_hidden')


@admin.register(Map)
class MapAdmin(PolymorphicChildModelAdmin):
    show_in_index = True


@admin.register(PostAbstract)
class PostAbstractAdmin(PolymorphicParentModelAdmin):
    base_model = PostAbstract
    list_filter = ('created_date', 'tags', PolymorphicChildModelFilter)
    list_display = ('title', 'created_date', 'modified_date', 'author')
    date_hierarchy = 'created_date'
    search_fields = ['title']
    child_models = (Post, Map)


@admin.register(Comment)
class CommentsAdmin(MPTTModelAdmin):
    mptt_level_indent = 10
    mptt_indent_field = 'get_short_text'
    list_filter = ['created_date']
    list_display = ('get_short_text', 'get_post', 'created_date', 'modified_date', 'author', 'is_deleted')
    date_hierarchy = 'created_date'
    search_fields = ['text']

    def get_post(self, obj):
        return obj.post.title

    get_post.short_description = 'Пост'

    def get_short_text(self, obj):
        return str(obj)

    get_short_text.short_description = 'Текст'
