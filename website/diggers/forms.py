import re
from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'category', 'tags', 'is_hidden')

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')

        for i, tag in enumerate(tags):
            tags[i] = re.sub(r'[^\w\s\d\-_,]', '', tag).lower()

        return tags
