document.addEventListener("DOMContentLoaded", function() {
    // Seleciona o botão de Categorias
    const dropdownButton = document.querySelector('.dropdown .button-like-link');

    // Seleciona o submenu
    const dropdownMenu = document.querySelector('.dropdown .dropdown-menu');

    // Adiciona evento para mostrar o submenu ao passar o mouse sobre Categorias
    dropdownButton.addEventListener('mouseenter', function() {
        dropdownMenu.style.display = 'block';
    });

    // Adiciona evento para esconder o submenu quando o mouse sai do botão e do menu
    dropdownButton.addEventListener('mouseleave', function() {
        dropdownMenu.style.display = 'none';
    });

    // Mantém o menu aberto enquanto o mouse está sobre ele
    dropdownMenu.addEventListener('mouseenter', function() {
        dropdownMenu.style.display = 'block';
    });

    // Esconde o menu quando o mouse sai do submenu
    dropdownMenu.addEventListener('mouseleave', function() {
        dropdownMenu.style.display = 'none';
    });
});
