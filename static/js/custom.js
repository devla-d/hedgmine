'use strict';

(function($) {
    /*------------------
        Background Set
    --------------------*/
    $('.set-bg').each(function() {
        var bg = $(this).data('setbg');
        //$(this).css('background-image', 'url(' + bg + ')');
        //$(this).css('background-image', 'linear-gradient( rgba(4, 34, 80, 0.8) 100%, rgba(4, 34, 80, 0.8)100%),url(' + bg + ') ');
        $(this).css('background-image', 'linear-gradient( rgba(0, 0, 0, 0.5) 100%, rgba(0, 0, 0, 0.5)100%),url(' + bg + ') ');

    });
    $('.set-bg2').each(function() {
        var bg = $(this).data('setbg');
        //$(this).css('background-image', 'url(' + bg + ')');
        $(this).css('background-image', 'linear-gradient(  rgba(10, 19, 32, 0.8) 100%, rgba(10, 19, 32, 0.8)100%),url(' + bg + ') ');
        //$(this).css('background-image', 'linear-gradient( rgba(0, 0, 0, 0.9) 100%, rgba(0, 0, 0, 0.9)100%),url(' + bg + ') ');

    });
    $('.set-bgwelcome').each(function() {
        var bg = $(this).data('setbg');
        $(this).css('background-image', 'url(' + bg + ')');

    });

    $(window).scroll(function() {
        if ($(this).scrollTop() > 100) {
            $('.header').addClass("animated slideInDown header-dark"), 1000;
        } else {
            $('.header').removeClass("animated slideInDown header-dark"), 1000;
        }
    });

    $('.sidebar-toggler').click(function() {
        $('.sidebar').removeClass('animated slideOutLeft').addClass('active animated slideInLeft ');

    });

    $('.dismis-bar').click(function() {
        $('.sidebar').removeClass('animated slideInLeft active').addClass('animated slideOutLeft');

    });


    /*
	    Wow
	*/
    new WOW().init();

})(jQuery);