function changeCurrent(item) {
    $('.current').removeClass('current')
    $('#current').removeAttr('id')
    $(item).addClass('current').attr('id', 'current')
}

function locateCurrent() {
    let current = document.querySelector("#current");
    if (current !== null) { current.scrollIntoView(true); }
}

$(document).ready(function () {
    const audio = document.querySelector('audio')
    audio.onended = function () {
        $.ajax({
            url: '/random', method: 'GET',
            success: function (res) {
                audio.src = '/music/' + res
                changeCurrent($('.item')[res])
                locateCurrent()
            },
            error: function (err) { if (err) alert(err.message) }
        })
    }

    $('.item').each(function (_, item) {
        $(item, '.content').on('click', function () {
            let id = $(this).attr('id')
            audio.src = '/music/' + id
            changeCurrent(item)
        })
    })

    $('#locate').on('click', locateCurrent)
})