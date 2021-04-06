document.addEventListener("DOMContentLoaded", function () {
    const fields = document.querySelectorAll('textarea[data-type=ckeditor]')
    fields.forEach(function (field) {
        CKEDITOR.replace(field.id, {
            language: 'uk',
            removeButtons: 'Cut,Copy,Paste,Anchor,Subscript,Superscript,About,Indent,Outdent',

            extraPlugins: 'embed,uploadimage,image2,sourcearea,table,maximize',

            // Load the default contents.css file plus customizations for this sample.
            contentsCss: [
                '/static/css/base.css',
                '/static/css/main.css'
            ],
            embed_provider: '//ckeditor.iframe.ly/api/oembed?url={url}&callback={callback}',

            image2_alignClasses: ['image-align-left', 'image-align-center', 'image-align-right'],
            image2_disableResizer: true,

            filebrowserUploadUrl: '/upload',
            filebrowserImageUploadUrl: '/upload',

            stylesSet: 'diggers:/static/ckeditor/styles_diggers.js',
            format_tags: 'p;h1;h2;h3;h4;h5;h6;div',
        });
    });
});

CKEDITOR.on('dialogDefinition', function( ev ) {
  const dialogName = ev.data.name;
  const dialogDefinition = ev.data.definition;

  if(dialogName === 'table') {
        const page = dialogDefinition.getContents('info');
        page.remove('txtCellSpace');
        page.remove('txtCellPad');
        page.remove('txtBorder');
        page.remove('txtHeight');
  }
});