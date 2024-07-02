$(document).ready(() => {
    $('.like-button').on('click', function () {
        const csrfToken = $('[name="csrfmiddlewaretoken"]').attr('value');
        const likeIcon = $(this);

        $.ajax({
            headers: {
                'X-CSRFToken': csrfToken,
            },
            url: "/like_toggle/",
            method: 'post',
            data: JSON.stringify({post_id: likeIcon.data('id')}),
            success: ({status}) => {
                const likeCount = likeIcon.next();

                if (status === "add like") {
                    likeIcon.removeClass('bi-heart').addClass('bi-heart-fill');
                    likeIcon.attr('title', 'unlike');
                    likeIcon.css('color', "#dc3545");
                    likeCount.text(parseInt(likeCount.text()) + 1);
                } else {
                    likeIcon.removeClass('bi-heart-fill').addClass('bi-heart');
                    likeIcon.attr('title', 'like');
                    likeIcon.css('color', "");
                    likeCount.text(parseInt(likeCount.text()) - 1);
                }
            },
            error: () => {
                alert('error');
            }
        })
    })
});