from django import forms


class CKEditorWidget(forms.Textarea):
    def __init__(self):
        super(CKEditorWidget, self).__init__(attrs={'data-type': 'ckeditor'})

    class Media:
        js = (
            'ckeditor/ckeditor.js',
            'ckeditor/init.js',
        )
