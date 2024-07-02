$(document).ready(() => {
    $('.edit-post').on('click', function (e) {
        const postId = $(this).data('id');
        const postContent = $(this).parents('.post').children('.post-content').text();

        const updateForm = $('#postUpdateForm');
        updateForm.children('[name=post_id]').val(postId);
        updateForm.children('[name=content]').val(postContent);
    })
});