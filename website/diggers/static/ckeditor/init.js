document.addEventListener("DOMContentLoaded", function () {
    const fields = document.querySelectorAll('textarea[data-type=ckeditor]')
    fields.forEach(function (field) {
        CKEDITOR.replace(field.id, {
            language: 'uk',
            removeButtons: 'Cut,Copy,Paste,Anchor,Subscript,Superscript',

            extraPlugins: 'embed,uploadimage,image2',

            // Load the default contents.css file plus customizations for this sample.
            contentsCss: '/static/ckeditor/contents.css',
            embed_provider: '//ckeditor.iframe.ly/api/oembed?url={url}&callback={callback}',

            image2_alignClasses: ['image-align-left', 'image-align-center', 'image-align-right'],
            image2_disableResizer: true,

            filebrowserUploadUrl: '/',
            filebrowserImageUploadUrl: '/',

            stylesSet: 'diggers:/static/ckeditor/styles_diggers.js'
        });
    });
});