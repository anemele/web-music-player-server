function changeCurrent(item) {
    $('.current').removeClass('current')
    $('#current').removeAttr('id')
    $(item).addClass('current').attr('id', 'current')
}

function locateCurrent() {
    let current = document.querySelector("#current");
    if (current !== null) { current.scrollIntoView(true); }
}

function randrange(max) {
    return Math.floor(Math.random() * max);
}

$(document).ready(function () {
    const audio = document.querySelector('audio')

    function play(id) {
        audio.src = '/music/' + id
        if (audio.paused) { audio.paused = false; audio.play() }
    }

    function next() {
        let id = randrange($('li.item').length)
        play(id)
        changeCurrent($(`.item[uid=${id}]`))
        locateCurrent()
    }

    audio.onended = next

    $('.item').each(function (_, item) {
        $(item, '.content').on('click', function () {
            if ($(this).attr('id') === 'current') { return }
            let id = $(this).attr('uid')
            play(id)
            changeCurrent(item)
        })
    })

    $('#locate').on('click', locateCurrent)
})