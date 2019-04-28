$(function() {

var userNumber = 0;

$('.read-more > .receive-text').click(function() {
$(this).hide();
$(this).parents('.message-group').children('.description').hide();
console.log($(this).parent().children(".card-container").fadeIn(500));

});

$(".receive-close-text").click(function() {
 $(this).parents('.card-container').hide();
 $(this).parents('.message-group').children('.description').fadeIn(200);
 $(this).parents('.read-more').children('.receive-text').fadeIn(200);
})

$('.sending-btn').click(function() {
$(this).parent().hide();
$(this).parents('tbody').find('.sending-text').fadeIn(200);
});

$('.sending-close-text').click(function() {
$(this).parent().hide();
$(this).parents('tbody').find('td').eq(0).show();
});

$('#receive').click(function() {
$(this).prop("disabled", false);
$(this).removeClass('btn-light');
$(this).addClass('btn-danger');
$('#send').removeClass('btn-primary');
$('#send').addClass('btn-light');
$('.receive-index').fadeIn(200);
$('.send-index').hide();
$('.user-index').hide();
$('.show-index').hide();
});

$('#send').click(function() {
$(this).prop("disabled", false);
$(this).removeClass('btn-light');
$(this).addClass('btn-primary');
$('#receive').removeClass('btn-danger');
$('#receive').addClass('btn-light');
$('.send-index').fadeIn(200);
$('.receive-index').hide();
$('.user-index').hide();
$('.show-index').hide();
});

$('#user-btn').click(function() {
$('.receive-index').hide();
$('.send-index').hide();
$('.user-index').fadeIn(200);
$('#receive').removeClass('btn-danger');
$('#receive').addClass('btn-light');
$('#send').removeClass('btn-primary');
$('#send').addClass('btn-light');
$('.show-card-' + userNumber).hide();
});

$('.user-thumb').click(function() {
$('.show-index').show();
userNumber = $(this).data('number');
console.log(userNumber);
$(this).parents('.user-index').hide();
$('.show-card-' + userNumber).fadeIn(200);
});


});