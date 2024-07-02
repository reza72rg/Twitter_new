function formSubmitter(e) {
    e.preventDefault();

    const csrfToken = $('[name="csrfmiddlewaretoken"]').attr('value');
    const formData = $(e.target).serializeArray();
    const data = {};

    $.map(formData, ({name, value}) => {
        data[name] = value;
    });

    $.ajax({
        headers: {
            'X-CSRFToken': csrfToken,
        },
        url: e.target.action,
        method: e.target.method,
        data: JSON.stringify(data),
        success: () => {
            alert('Successful!')
            location.reload();
        },
        error: (e) => {
            alert(e.responseJSON.error);
        }
    });
}