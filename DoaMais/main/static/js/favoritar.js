document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.star-rating').forEach(function(star) {
        star.addEventListener('click', function() {
            const itemId = this.getAttribute('data-item-id');
            fetch("{% url 'favoritos' %}", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
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
            .catch(error => {
                console.error('Error:', error);
                // Reverter visualmente o estado se houver erro na atualização
                this.classList.toggle('selected');
            });
        });
    });
});
