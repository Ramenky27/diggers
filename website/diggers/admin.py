from django.contrib import admin, messages
from django import forms
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter
from django.contrib.auth.admin import UserAdmin
from mptt.admin import MPTTModelAdmin

from .models import User, Post, Comment, Category, PostAbstract, Map
from .views import HTMLActivationEmailMixin
from .widgets import CKEditorWidget


# Register your models here.


class EmailActivation(HTMLActivationEmailMixin):
    def __init__(self, **kwargs):
        super(EmailActivation, self).__init__()
        self.request = kwargs.get('request')


def send_activation(modeladmin, request, queryset):
    for user in queryset:
        EmailActivation(request=request).send_activation_email(user)

    messages.add_message(request, messages.INFO, 'Код підтвердження надіслано обраним користувачам')


send_activation.short_description = 'Надіслати код підтвердження'


class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'title', 'text', 'category', 'tags', 'is_hidden']
        widgets = {
            'text': CKEditorWidget(),
        }


class MapAdminForm(forms.ModelForm):
    class Meta:
        model = Map
        fields = ['author', 'title', 'file', 'description', 'tags']
        widgets = {
            'description': CKEditorWidget(mode='simple'),
        }


class CommentAdminForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['post', 'author', 'text', 'parent', 'is_deleted']
        widgets = {
            'text': CKEditorWidget(mode='simple'),
        }


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


@admin.register(PostAbstract)
class PostAbstractAdmin(PolymorphicParentModelAdmin):
    base_model = PostAbstract
    list_filter = ('created_date', 'tags', PolymorphicChildModelFilter, 'is_hidden')
    list_display = ('title', 'created_date', 'modified_date', 'author', 'is_hidden')
    date_hierarchy = 'created_date'
    search_fields = ['title']
    child_models = (Post, Map)


@admin.register(Post)
class PostAdmin(PolymorphicChildModelAdmin):
    show_in_index = True
    form = PostAdminForm


@admin.register(Map)
class MapAdmin(PolymorphicChildModelAdmin):
    show_in_index = True
    form = MapAdminForm


@admin.register(Comment)
class CommentsAdmin(MPTTModelAdmin):
    mptt_level_indent = 10
    mptt_indent_field = 'get_short_text'
    list_filter = ['created_date']
    list_display = ('get_short_text', 'get_post', 'created_date', 'modified_date', 'author', 'is_deleted')
    date_hierarchy = 'created_date'
    search_fields = ['text']
    form = CommentAdminForm

    def get_post(self, obj):
        return obj.post.title

    get_post.short_description = 'Пост'

    def get_short_text(self, obj):
        return str(obj)

    get_short_text.short_description = 'Текст'
