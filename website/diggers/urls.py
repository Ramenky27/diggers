from django.urls import path
from django.views.generic.base import TemplateView
from django.contrib.auth.views import PasswordResetView

from . import views
from .forms import ExtendedRegistrationForm

app_name = 'diggers'
urlpatterns = [
    path('', views.PostList.as_view(), name='post_list'),
    path('category/<str:category>/', views.PostList.as_view(), name='list_by_category'),
    path('tags/<str:tags>/', views.PostList.as_view(), name='list_by_tags'),
    path('posts/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('posts/new', views.PostCreate.as_view(), name='post_create'),
    path('posts/<int:pk>/edit', views.PostUpdate.as_view(), name='post_update'),
    path('posts/<int:pk>/delete', views.PostDelete.as_view(), name='post_delete'),

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
]