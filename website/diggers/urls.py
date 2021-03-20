from django.urls import path, include
from django_registration.backends.activation.views import RegistrationView

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

    path('accounts/register/',
         RegistrationView.as_view(
             form_class=ExtendedRegistrationForm
         ),
         name='django_registration_register',
         ),
    path('accounts/login/', views.ExtendedLoginView.as_view(), name='login'),
    path('accounts/', include('django_registration.backends.activation.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]