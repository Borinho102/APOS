$(function () {
    $('[data-toggle="popover"]').popover()
});
$(function () {
    $('.example-popover').popover({
        container: 'body'
    })
});
// Chargement de la Page
$(window).scroll(function(){
    if ($(this).scrollTop() > 100) {
        $('.scrollup').fadeIn();
    } else {
        $('.scrollup').fadeOut();
    }
});
$('.scrollup').click(function(){
    $("html, body").animate({
        scrollTop: 0
        }, 1000);
    return false;
});
$(window).load(function () {
    $(".loaded").fadeOut();
    $(".preloader").delay(1000).fadeOut("slow");
});
$("#menu-toggle").click(function(e) {
    e.preventDefault();
    $("#wrapper").toggleClass("toggled");
    if($(this).hasClass('glyphicon-menu-left')){
        $(this).removeClass('glyphicon-menu-left').addClass('glyphicon-menu-right');
    }
    else{
        $(this).removeClass('glyphicon-menu-right').addClass('glyphicon-menu-left');
    }
});

function clear(option){
    if(option === 0){
        $('#filter').css('display', 'none');
    }
    $('#ecole').css('display', 'none');
    $('#filiere').css('display', 'none');
    $('#concours').css('display', 'none');
}

function cls(id) {
    $('#' + id).fadeOut('slow').hide();
}

function display(id){
    clear(0);
    $('#filter').fadeIn('slow').css('display', 'block');
    setTimeout(function () {
        $('#' + id).fadeIn('slow').show('slow');
    }, 300);
}
$(document).ready(function () {
    clear(0);
});

// Bouton radio de recherche
$('#school').change(function () {
    if(this.checked){
        clear(1);
        display("ecole");
    }
    else{
        cls("ecole");
    }
});
$('#branch').change(function () {
    if(this.checked){
        clear(1);
        display("filiere");
    }
    else{
        cls("filiere");
    }
});
$('#exam').change(function () {
    if(this.checked){
        clear(1);
        display("concours");
    }
    else{
        cls("concours");
    }
});
$('#all').change(function () {
    if(this.checked){
        clear(0);
    }
});