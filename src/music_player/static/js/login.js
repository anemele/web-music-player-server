$(document).ready(function () {

    $('#password').bind('keydown', function (event) {
        if (event.keyCode == '13') /* Enter */ {

            let pwd = $(this).val().trim()
            if (pwd === '') {
                return
            }

            $.ajax({
                url: '/login',
                method: 'POST',
                data: { pwd },
                success: function (res) {
                    if (res.code == 0) { window.location.pathname = '/music' }
                    else { alert(res.msg) }
                }
            })
        }
    })
})