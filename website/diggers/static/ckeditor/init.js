const defaultConfig = {
    language: 'uk',
    removeButtons: 'Cut,Copy,Paste,Anchor,Subscript,Superscript,About,Indent,Outdent',
    extraPlugins: 'embed,image2,sourcearea,table,maximize',
    removePlugins: '',

    embed_provider: '//ckeditor.iframe.ly/api/oembed?url={url}&callback={callback}',

    image2_alignClasses: ['image-align-left', 'image-align-center', 'image-align-right'],
    image2_disableResizer: true,

    contentsCss: [
        '/static/css/base.css',
        '/static/css/main.css'
    ],

    stylesSet: 'diggers:/static/ckeditor/styles_diggers.js',
    format_tags: 'p;h1;h2;h3;h4;h5;h6;div',
};

const simpleConfig = Object.assign({}, defaultConfig, {
    removeButtons: 'Cut,Copy,Paste,Format,Styles,Undo,Redo,Anchor,Subscript,Superscript,About,Indent,Outdent',
    extraPlugins: 'embed,image2,sourcearea',
    removePlugins: 'table,maximize,exportpdf,autosave',
});

document.addEventListener("DOMContentLoaded", function () {
    const fields = document.querySelectorAll('textarea[data-type=ckeditor]')
    fields.forEach(function (field) {
        let config;
        if (field.dataset.mode === 'simple') {
            config = simpleConfig;
        } else {
            config = defaultConfig;
        }
        CKEDITOR.replace(field.id, config);
    });
});

CKEDITOR.on('dialogDefinition', function (ev) {
    const dialogName = ev.data.name;
    const dialogDefinition = ev.data.definition;

    if (dialogName === 'table') {
        const page = dialogDefinition.getContents('info');
        page.remove('txtCellSpace');
        page.remove('txtCellPad');
        page.remove('txtBorder');
        page.remove('txtHeight');
    }
});