document.addEventListener('DOMContentLoaded', function() {
    const stars = document.querySelectorAll('.star-rating label');

    stars.forEach(label => {
        label.addEventListener('click', function() {
            const allLabels = this.parentNode.querySelectorAll('label');
            const radioButtons = this.parentNode.querySelectorAll('input[type="radio"]');
            let clickedLabelIndex = Array.from(allLabels).indexOf(this);
            
            // Define a cor de todas as estrelas até a clicada para amarelo
            radioButtons.forEach((radio, index) => {
                if (index <= clickedLabelIndex) {
                    allLabels[index].style.color = 'yellow'; // Muda a cor das estrelas para amarelo
                } else {
                    allLabels[index].style.color = 'grey'; // Reverte a cor das estrelas não selecionadas
                }
            });
        });
    });
});
