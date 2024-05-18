document.querySelectorAll('.favorite-icon').forEach(icon => {
    icon.addEventListener('click', function() {
        const itemId = this.dataset.itemId;
        const isFavorite = this.src.includes('star-filled.png');
        
        // Alternar a imagem da estrela
        this.src = isFavorite ? '../static/imagens/star-empty.png' : '../static/imagens/star-filled.png';

        // Enviar a requisição AJAX
        fetch(`{% url 'pesquisar' %}`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}',
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ item_id: itemId })
        })
        .then(response => response.json())
        .then(data => console.log(data.message))
        .catch(error => console.error('Error:', error));
    });
});
