$(document).ready(function () {
    $('#login').on('click', function () {
        let pwd = $('#password').val().trim()
        if (pwd === '') {
            return
        }
        $.ajax({
            url: '/login',
            method: 'POST',
            data: { pwd },
            success: function (res) {
                if (res.code == 0) { window.location.pathname = '/' }
                else { alert('密码错误') }
            }
        })
    })
})