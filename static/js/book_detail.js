function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

$(document).ready(function () {
    $('#review-form').on('submit', function (e) {
        e.preventDefault();

        const form = $(this);
        const url = form.attr('action');
        const formData = form.serialize();

        $.ajax({
            url: url,
            method: 'POST',
            data: formData,
            headers: { 'X-CSRFToken': csrftoken },
            success: function (data) {
                $('#reviews-container p:contains("Brak recenzji")').remove();
                $('#reviews-container').append(data.review_html);
                $('[data-avg-rating]').html(`<i class="bi bi-star-fill"></i> ${data.avg_rating}`);
                form.remove();
                $('#review-info').html('<p class="text-muted">Już dodałeś recenzję tej książki.</p>');
            },
            error: function (xhr) {
                const err = xhr.responseJSON;
                alert(err?.error || 'Wystąpił błąd');
            }
        });
    });
});