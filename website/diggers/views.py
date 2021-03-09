from django.views import generic
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Category, User, Post

# Create your views here.


class PostList(generic.ListView):
    paginate_by = settings.POSTS_PER_PAGE
    context_object_name = 'posts'

    def get_queryset(self):
        query = {}

        if 'category' in self.kwargs:
            query['category'] = get_object_or_404(Category, route=self.kwargs['category'])

        if 'tags' in self.kwargs:
            query['tags__name__in'] = self.kwargs['tags'].split(",")

        if 'author' in self.kwargs:
            query['author__pk'] = get_object_or_404(User, username=self.kwargs['author'])

        if not self.request.user.has_perm('diggers.hidden_access'):
            query['is_hidden'] = False

        q = {k: v for k, v in query.items() if v is not None}

        return Post.objects.filter(Q(**q)).distinct().order_by('-created_date')


class PostDetail(generic.DetailView):
    model = Post


class PostCreate(LoginRequiredMixin, generic.CreateView):
    model = Post
    fields = ['title', 'text', 'category', 'tags', 'is_hidden']


class PostUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Post
    fields = ['title', 'text', 'category', 'tags', 'is_hidden']
    template_name_suffix = '_update_form'


class PostDelete(LoginRequiredMixin, generic.DeleteView):
    model = Post
    fields = ['title', 'text', 'category', 'tags', 'is_hidden']
    template_name_suffix = reverse_lazy('index')
