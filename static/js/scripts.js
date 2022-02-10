$(document).ready(function() {


    /* csrf token */
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    const next_earning_date = $('#next_earning_date');
    console.log(csrftoken)
    const timer = next_earning_date.attr('data-date');
    if (timer) {

        const eventDate = Date.parse(timer);
        // Update the count down every 1 second
        var x = setInterval(function() {
            // Get today's date and time
            var now = new Date().getTime();

            // Find the distance between now and the count down date
            var distance = eventDate - now;
            // Time calculations for days, hours, minutes and seconds
            var days = Math.floor(distance / (1000 * 60 * 60 * 24));
            var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            var seconds = Math.floor((distance % (1000 * 60)) / 1000);



            next_earning_date.text(`${hours}h :${minutes}m :${seconds}s`)

            if (distance < 0) {
                clearInterval(x);
                next_earning_date.text(`0 h 0 m 0 s`)
                user_daily_income()


            }

        }, 1000)

    }

    function user_daily_income() {
        $.ajax({
            type: "POST",
            url: "/credit-user/",
            data: {
                user_id: '{{ user.id }}',
                csrfmiddlewaretoken: csrftoken,
            },

            success: function(data) {
                var resp = data
                toastr.success(`${data.msg}`, {
                    // timeOut: 500000,
                    closeButton: !0,
                    debug: !1,
                    newestOnTop: !0,
                    progressBar: !0,
                    positionClass: "toast-top-right demo_rtl_class",
                    preventDuplicates: !0,
                    onclick: null,
                    showDuration: "300",
                    hideDuration: "1000",
                    extendedTimeOut: "1000",
                    showEasing: "swing",
                    hideEasing: "linear",
                    showMethod: "fadeIn",
                    hideMethod: "fadeOut",
                    tapToDismiss: !1,
                    closeHtml: '<div class="circle_progress"></div><span class="progress_count"></span> <i class="la la-close"></i>'
                });
                setTimeout(function() { window.location.reload(); }, 1300);

            },

        });
    }

});