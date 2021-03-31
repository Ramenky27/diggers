from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from django.contrib.auth.views import PasswordResetView

from . import views
from .forms import ExtendedRegistrationForm

app_name = 'diggers'
urlpatterns = [
    path('', views.PostList.as_view(), name='post_list'),
    path('category/maps/', views.MapList.as_view(), name='map_list'),
    path('tags/<str:tags>/', views.PostList.as_view(), name='list_by_tags'),
    path('category/<str:category>/', views.PostListByObject.as_view(), name='list_by_category'),
    path('author/<str:author>/', views.PostListByObject.as_view(), name='list_by_author'),

    path('posts/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('posts/new/', views.PostCreate.as_view(), name='post_create'),
    path('posts/<int:pk>/edit/', views.PostUpdate.as_view(), name='post_update'),
    path('posts/<int:pk>/delete/', views.PostDelete.as_view(), name='post_delete'),

    path('maps/new/', views.MapCreate.as_view(), name='map_create'),
    path('map/<int:pk>/', views.MapDownload.as_view(), name='map_download'),

    path('posts/<int:pk>/comment/new/', views.CommentCreate.as_view(), name='comment_create'),
    path('comment/<int:cpk>/answer/', views.CommentCreate.as_view(), name='comment_answer'),
    path('comment/<int:pk>/edit/', views.CommentUpdate.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', views.CommentDelete.as_view(), name='comment_delete'),

    path(
        'accounts/activate/complete/',
        TemplateView.as_view(
            template_name='registration/activation_complete.html'
        ),
        name='registration_activation_complete',
    ),
    path(
        'accounts/activate/<str:activation_key>/',
        views.EmailActivationView.as_view(),
        name='registration_activate',
    ),
    path('accounts/register/',
         views.ExtendedRegistrationView.as_view(
             form_class=ExtendedRegistrationForm
         ),
         name='registration',
         ),
    path('accounts/login/', views.ExtendedLoginView.as_view(), name='login'),
    path(
        'accounts/password_reset/',
        PasswordResetView.as_view(
            html_email_template_name='registration/password_reset_email.html',
            email_template_name='registration/password_reset_email.txt'
        ),
        name='password_reset'
    ),
    path('accounts/profile/', views.PostListByObject.as_view(by_current_user=True), name='profile'),
    path('accounts/profile/edit/', views.ProfileEditView.as_view(), name='profile_update')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)