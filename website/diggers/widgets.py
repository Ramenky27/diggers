from django import forms


class CKEditorWidget(forms.Textarea):
    def __init__(self, **kwargs):
        mode = kwargs.get('mode')
        if not mode:
            mode = 'extended'
        super(CKEditorWidget, self).__init__(attrs={'data-type': 'ckeditor', 'data-mode': mode})

    class Media:
        js = (
            'ckeditor/ckeditor.js',
            'ckeditor/init.js',
        )
