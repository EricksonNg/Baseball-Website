// Transform regular html selection form to jquery select2 form
$(document).ready(function(){
    $( '#name' ).select2({width:"style"});
    $( '#team' ).select2({width : "style"});
    $( '#cType' ).select2({width : "style"});
    $( '#category' ).select2({});
    $( '#loadingMask' ).fadeOut(500);
});