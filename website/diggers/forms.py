import re
from django import forms
from django_registration.forms import RegistrationForm

from .models import Post, User


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        template_name = 'diggers/blocks/form.html'
        fields = ['title', 'text', 'category', 'tags', 'is_hidden']

    def __init__(self, *args, **kwargs):
        self.author = kwargs['initial']['author']
        super(PostForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        obj = super(PostForm, self).save(commit=False)
        obj.author = self.author

        if commit:
            obj.save()
            self.save_m2m()

        return obj

    def clean(self):
        cleaned_data = super().clean()

        tags = cleaned_data.get('tags')

        for i, tag in enumerate(tags):
            tags[i] = re.sub(r'[^\w\s\d\-_,]', '', tag).lower()

        cleaned_data['tags'] = tags

        return cleaned_data


class ExtendedRegistrationForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = User
