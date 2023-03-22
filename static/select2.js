// Transform regular html selection form to jquery select2 form
$(document).ready(function(){
    $( '#year' ).select2({width:"style"});
    $( '#name' ).select2({width:"style"});
    $( '#team' ).select2({width : "style"});
    $( '#cType' ).select2({width : "style"});
    $( '#category' ).select2({});
    $( '#batSide' ).select2({width: "style"});
    $( '#loadingMask' ).fadeOut(500);
});