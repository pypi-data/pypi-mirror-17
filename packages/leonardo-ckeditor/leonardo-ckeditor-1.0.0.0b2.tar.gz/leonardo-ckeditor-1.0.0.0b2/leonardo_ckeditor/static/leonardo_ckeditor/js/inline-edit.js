var ck = CKEDITOR.inline('web-htmltextwidget-26-23');

ck.on( 'instanceReady', function( ev ) {
     var editor = ev.editor;
     editor.setReadOnly( false );
});