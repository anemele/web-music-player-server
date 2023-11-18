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
                changeCurrent($(`.item[uid=${res}]`))
                locateCurrent()
            },
            error: function (err) { if (err) alert(err) }
        })
    }

    $('.item').each(function (_, item) {
        $(item, '.content').on('click', function () {
            if ($(this).attr('id') === 'current') { return }
            let id = $(this).attr('uid')
            audio.src = '/music/' + id
            changeCurrent(item)
            if (audio.paused) { audio.paused = false; audio.play() }
        })
    })

    $('#locate').on('click', locateCurrent)
})