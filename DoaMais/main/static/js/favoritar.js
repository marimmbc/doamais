document.addEventListener('DOMContentLoaded', function() {
    const csrftoken = getCookie('csrftoken');

    document.querySelectorAll('.star-rating .star').forEach(function(star) {
        star.addEventListener('click', function() {
            const itemId = this.parentElement.getAttribute('data-item-id');
            fetch("{% url 'categoria_roupas' %}", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({ 'item_id': itemId })
            })
            .then(response => response.json())
            .then(data => {
                if (data.favorited) {
                    this.classList.add('selected');
                } else {
                    this.classList.remove('selected');
                }
            })
        });
    });

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
});
