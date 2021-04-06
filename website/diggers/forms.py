import re
from django import forms
from django_registration.forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from captcha.fields import CaptchaField

from .models import User, Comment, Post, Map
from .widgets import CKEditorWidget


class PostAbstractForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.author = kwargs['initial']['author']
        super(PostAbstractForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        tags = cleaned_data.get('tags')

        for i, tag in enumerate(tags):
            tags[i] = re.sub(r'[^\w\s\d\-_,]', '', tag).lower()

        cleaned_data['tags'] = tags

        return cleaned_data


class AttachCurrentUserMixin(forms.ModelForm):
    def save(self, commit=True):
        obj = super(AttachCurrentUserMixin, self).save(commit=False)
        obj.author = self.author

        if commit:
            obj.save()
            self.save_m2m()

        return obj


class PostForm(PostAbstractForm):
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['category'].empty_label = None
        self.fields['category'].required = True
        self.fields['text'].widget = CKEditorWidget()
        if not self.author.has_perm('diggers.hidden_access'):
            self.fields['is_hidden'].widget = forms.HiddenInput()

    class Meta:
        model = Post
        fields = ['title', 'text', 'category', 'tags', 'is_hidden']


class MapForm(PostAbstractForm):
    def __init__(self, *args, **kwargs):
        super(MapForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget = CKEditorWidget(mode='simple')

    class Meta:
        model = Map
        fields = ['title', 'file', 'description', 'tags']


class PostCreateForm(AttachCurrentUserMixin, PostForm):
    pass


class MapCreateForm(AttachCurrentUserMixin, MapForm):
    pass


class CommentCreateForm(forms.ModelForm):
    parent = None

    class Meta:
        model = Comment
        fields = ['text']

    def __init__(self, *args, **kwargs):
        self.author = kwargs['initial']['author']
        self.post = kwargs['initial']['post']
        if 'parent' in kwargs['initial']:
            self.parent = kwargs['initial']['parent']

        super(CommentCreateForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget = CKEditorWidget(mode='simple')

    def save(self, commit=True):
        obj = super(CommentCreateForm, self).save(commit=False)
        obj.author = self.author
        obj.post = self.post

        if self.parent:
            obj.parent = self.parent

        if commit:
            obj.save()
            self.save_m2m()

        return obj


class ExtendedRegistrationForm(RegistrationForm):
    captcha = CaptchaField()

    class Meta(RegistrationForm.Meta):
        model = User
        fields = [
            User.USERNAME_FIELD,
            User.get_email_field_name(),
            "password1",
            "password2",
            "avatar",
            "birth_date",
            "location",
            "captcha"
        ]
        widgets = {
            'birth_date': forms.widgets.DateInput(attrs={'type': 'date'})
        }


class ExtendedLoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, label='Запам’ятати мене')


class ProfileForm(forms.ModelForm):
    class Meta(RegistrationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'email', 'avatar', 'birth_date', 'location']
        widgets = {
            'birth_date': forms.widgets.DateInput(attrs={'type': 'date'})
        }
