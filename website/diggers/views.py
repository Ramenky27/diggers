from django.views import generic
from django.db.models import Q
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from next_prev import next_in_order, prev_in_order

from django.contrib.auth.views import LoginView
from django_registration.backends.activation.views import ActivationView, RegistrationView as ActivationEmailMixin
from django_registration.backends.one_step.views import RegistrationView as OneStepRegistrationView
from django_registration.exceptions import ActivationError
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.contrib.sitemaps import Sitemap

from .models import Category, User, Comment, PostAbstract, Post, Map
from .forms import PostCreateForm, MapCreateForm, PostForm, MapForm, ExtendedLoginForm, ProfileForm, \
    CommentCreateForm, CommentUpdateForm


# Create your views here.


class CheckUserVerifiedMixin(UserPassesTestMixin, generic.View):
    def test_func(self):
        return self.request.user.email_verified is True


class HiddenAccessMixin(UserPassesTestMixin, generic.detail.SingleObjectMixin, generic.View):
    def test_func(self):
        obj = self.get_object()
        if obj.is_hidden:
            return self.request.user.has_perm('diggers.hidden_access')

        return True


class OwnerCheckMixin(UserPassesTestMixin, generic.detail.SingleObjectMixin, generic.View):
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class CheckModifyPermissionsMixin(CheckUserVerifiedMixin, OwnerCheckMixin, HiddenAccessMixin):
    object = None

    def get_object(self, queryset=None):
        if self.object:
            return self.object

        return super().get_object(queryset=queryset)

    def test_func(self):
        return CheckUserVerifiedMixin.test_func(self) \
               and OwnerCheckMixin.test_func(self) \
               and HiddenAccessMixin.test_func(self)


class PostList(generic.ListView):
    template_name = 'diggers/post_list.html'
    paginate_by = settings.POSTS_PER_PAGE
    context_object_name = 'posts'
    model = PostAbstract
    ordering = ['-created_date', '-pk']

    def get_context_data(self, **kwargs):
        ctx = super(PostList, self).get_context_data(**kwargs)
        if 'tags' in self.kwargs:
            ctx['tags'] = self.kwargs['tags']

        return ctx

    def get_queryset(self):
        query = {}
        if 'tags' in self.kwargs:
            query['tags__name__in'] = self.kwargs['tags'].split(",")

        if not self.request.user.has_perm('diggers.hidden_access'):
            query['is_hidden'] = False
            query['instance_of'] = Post

        q = {k: v for k, v in query.items() if v is not None}
        return super(PostList, self).get_queryset().filter(Q(**q))


class MapList(UserPassesTestMixin, PostList):
    model = Map

    def test_func(self):
        return self.request.user.has_perm('diggers.hidden_access')

    def get_context_data(self, **kwargs):
        ctx = super(MapList, self).get_context_data(**kwargs)
        ctx['category'] = {
            'name': 'Мапи',
            'route': 'maps',
        }
        return ctx

    def get_queryset(self):
        return super(MapList, self).get_queryset().filter(instance_of=Map)


class PostListByObject(generic.detail.SingleObjectMixin, PostList):
    query_pk_and_slug = True
    slug_url_kwarg = None
    slug_field = None
    object = None
    by_current_user = False
    model = PostAbstract

    def __init__(self, **kwargs):
        super().__init__()
        self.by_current_user = kwargs.get('by_current_user') is True

    def get(self, request, *args, **kwargs):
        model = None
        if 'category' in kwargs:
            self.slug_url_kwarg = 'category'
            self.slug_field = 'route'
            model = Category
        elif 'author' in kwargs or self.by_current_user:
            self.slug_url_kwarg = 'author'
            self.slug_field = 'username'
            model = User
            if self.by_current_user:
                self.kwargs['author'] = request.user.username

        self.object = self.get_object(queryset=model.objects.all())
        return super(PostList, self).get(request, *args, **kwargs)

    def get_queryset(self):
        query = {}
        if isinstance(self.object, User):
            query['author__pk'] = self.object.pk
        elif isinstance(self.object, Category):
            query['category'] = self.object

        q = {k: v for k, v in query.items() if v is not None}

        return PostList.get_queryset(self).filter(Q(**q))

    def get_context_data(self, **kwargs):
        ctx = super(PostListByObject, self).get_context_data(**kwargs)
        ctx[self.slug_url_kwarg] = self.object
        ctx['posts'] = self.object_list

        return ctx


class PostAbstractCreate(generic.CreateView):
    model = PostAbstract
    template_name_suffix = '_create_form'

    def get_initial(self):
        self.initial.update({'author': self.request.user})
        return self.initial


class PostDetail(HiddenAccessMixin, generic.DetailView):
    model = PostAbstract
    context_object_name = 'post'
    template_name = "diggers/post_detail.html"
    object = None

    def get_context_data(self, **kwargs):
        ctx = super(PostDetail, self).get_context_data(**kwargs)
        current = ctx['post']

        if self.request.user.is_authenticated and self.request.user.email_verified is True:
            ctx['form'] = CommentCreateForm(initial={
                'author': self.request.user,
                'post': self.object
            })

        query = {}
        if not self.request.user.has_perm('diggers.hidden_access'):
            query['is_hidden'] = False
            query['instance_of'] = Post

        q = {k: v for k, v in query.items() if v is not None}

        qs = Post.objects.filter(Q(**q)).order_by('created_date', 'pk')
        ctx['next_post'] = next_in_order(current, qs=qs)
        ctx['prev_post'] = prev_in_order(current, qs=qs)
        return ctx


class MapDownload(HiddenAccessMixin, generic.DetailView):
    model = Map
    object = None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        response = HttpResponse(self.object.file, content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename="{name}"'.format(name=self.object.file.name)
        return response


class PostCreate(LoginRequiredMixin, CheckUserVerifiedMixin, PostAbstractCreate):
    model = Post
    form_class = PostCreateForm


class MapCreate(LoginRequiredMixin, CheckUserVerifiedMixin, PostAbstractCreate):
    model = Map
    form_class = MapCreateForm


class PostUpdate(LoginRequiredMixin, CheckModifyPermissionsMixin, generic.UpdateView):
    model = PostAbstract
    template_name_suffix = '_update_form'
    object = None

    def get_initial(self):
        self.initial.update({'author': self.request.user})
        return self.initial

    def get_form_class(self):
        if isinstance(self.object, Map):
            return MapForm

        return PostForm


class PostDelete(LoginRequiredMixin, CheckModifyPermissionsMixin, generic.DeleteView):
    model = PostAbstract
    template_name_suffix = '_confirm_delete'
    success_url = reverse_lazy('diggers:post_list')


class ExtendedLoginView(LoginView):
    form_class = ExtendedLoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        remember_me = form.cleaned_data['remember_me']
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return super(ExtendedLoginView, self).form_valid(form)


class HTMLActivationEmailMixin(ActivationEmailMixin):
    plain_email_body_template = "django_registration/activation_email_body.txt"
    html_email_body_template = "django_registration/activation_email_body.html"

    def send_activation_email(self, user):
        activation_key = self.get_activation_key(user)
        context = self.get_email_context(activation_key)
        context["user"] = user
        subject = render_to_string(
            template_name=self.email_subject_template,
            context=context,
            request=self.request,
        )
        subject = "".join(subject.splitlines())
        message = render_to_string(
            template_name=self.plain_email_body_template,
            context=context,
            request=self.request,
        )
        html_message = render_to_string(
            template_name=self.html_email_body_template,
            context=context,
            request=self.request,
        )
        user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL, html_message=html_message)


class ExtendedRegistrationView(OneStepRegistrationView, HTMLActivationEmailMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            redirect_to = reverse_lazy('diggers:post_list')
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)

    def register(self, form):
        new_user = super(ExtendedRegistrationView, self).register(form)
        self.send_activation_email(new_user)
        return new_user


class EmailActivationView(ActivationView):
    success_url = reverse_lazy("diggers:registration_activation_complete")

    def activate(self, *args, **kwargs):
        username = self.validate_key(kwargs.get("activation_key"))
        user = self.get_user(username)
        user.email_verified = True
        user.save()
        return user

    def get_user(self, username):
        try:
            user = User.objects.get(**{User.USERNAME_FIELD: username})
            if user.email_verified:
                raise ActivationError(
                    self.ALREADY_ACTIVATED_MESSAGE, code="already_activated"
                )
            return user
        except User.DoesNotExist:
            raise ActivationError(self.BAD_USERNAME_MESSAGE, code="bad_username")


class ProfileEditView(LoginRequiredMixin, generic.UpdateView):
    form_class = ProfileForm
    template_name_suffix = '_update_form'

    def get_object(self, queryset=None):
        pk = self.request.user.pk
        return User.objects.filter(pk=pk).get()


class CommentCreate(LoginRequiredMixin, CheckUserVerifiedMixin, generic.CreateView):
    model = Comment
    form_class = CommentCreateForm
    template_name_suffix = '_create_form'

    def get_context_data(self, **kwargs):
        ctx = super(CommentCreate, self).get_context_data(**kwargs)
        ctx['parent'] = self.initial.get('parent')
        return ctx

    def get_initial(self):
        if 'cpk' in self.kwargs:
            parent = get_object_or_404(Comment, pk=self.kwargs.get('cpk'), is_deleted=False)
            self.initial.update({'parent': parent})
            post = parent.post
        else:
            post = get_object_or_404(PostAbstract, pk=self.kwargs.get('pk'))

        self.initial.update({
            'author': self.request.user,
            'post': post
        })
        return self.initial

    def test_func(self):
        if self.initial.get('post').is_hidden:
            return self.request.user.has_perm('diggers.hidden_access') and super(CommentCreate, self).test_func()

        return super(CommentCreate, self).test_func()

    def dispatch(self, request, *args, **kwargs):
        self.initial = self.get_initial()

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return "{url}#comment{pk}".format(
            url=reverse_lazy('diggers:post_detail', kwargs={'pk': self.object.post.pk}),
            pk=self.object.pk
        )


class CommentUpdate(LoginRequiredMixin, CheckModifyPermissionsMixin, generic.UpdateView):
    model = Comment
    form_class = CommentUpdateForm
    template_name_suffix = '_update_form'

    def get_queryset(self):
        qs = super(CommentUpdate, self).get_queryset()
        return qs.filter(is_deleted=False)

    def get_success_url(self):
        return "{url}#comment{pk}".format(
            url=reverse_lazy('diggers:post_detail', kwargs={'pk': self.object.post.pk}),
            pk=self.object.pk
        )


class CommentDelete(LoginRequiredMixin, CheckModifyPermissionsMixin, generic.DeleteView):
    model = Comment
    template_name_suffix = '_confirm_delete'
    object = None

    def get_queryset(self):
        qs = super(CommentDelete, self).get_queryset()
        return qs.filter(is_deleted=False)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.save(update_fields=['is_deleted'])
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        return reverse_lazy('diggers:post_detail', kwargs={'pk': self.object.post.pk})


class PostsSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Post.objects.filter(is_hidden=False).order_by('-created_date', '-pk')

    def lastmod(self, obj):
        return obj.created_date


class CategoriesSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Category.objects.all().order_by('name')


class StaticSitemap(Sitemap):
    changefreq = 'never'
    priority = 0.6

    def location(self, item):
        return reverse(item)
