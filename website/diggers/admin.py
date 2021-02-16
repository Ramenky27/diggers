from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from .models import User, Post, Comment, Category, Map
from mptt.admin import MPTTModelAdmin


# Register your models here.


def send_activation(request, queryset):
    for user in queryset:
        pass

    messages.add_message(request, messages.INFO, 'Код підтвердження надіслано обраним користувачам')


send_activation.short_description = 'Надіслати код підтвердження'


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


class CategoryAdmin(admin.ModelAdmin):
    base_model = Category
    list_display = ('name', 'route')
    ordering = ('name', 'route')


class PostAbstractAdmin(admin.ModelAdmin):
    list_filter = ('created_date', 'tags')
    list_display = ('title', 'created_date', 'modified_date', 'author')
    date_hierarchy = 'created_date'
    search_fields = ['title']


class PostAdmin(PostAbstractAdmin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.list_filter = self.list_filter + ('category',)
        self.list_display = self.list_display + ('category',)


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


admin.site.register(User, DiggersUserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Map, PostAbstractAdmin)
admin.site.register(Comment, CommentsAdmin)
