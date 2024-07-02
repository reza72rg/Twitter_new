function followToggle(user_id) {
    const csrfToken = $('[name="csrfmiddlewaretoken"]').attr('value');
    $.ajax({
        headers: {
            'X-CSRFToken': csrfToken,
        },
        url: '/follow_toggle/',
        method: 'post',
        data: JSON.stringify({user_id}),
        success: () => {
            location.reload();
        },
        error: () => {
            alert('error');
        }
    })
}