document.addEventListener('DOMContentLoaded', function() {
    fetch('../templates/navbar.html') 
      .then(response => response.text())
      .then(data => {
        document.getElementById('navbar-placeholder').innerHTML = data;

        // Inicializa o JavaScript necessário após carregar a navbar
        const navOpenBtn = document.querySelector(".navOpenBtn"),
            navCloseBtn = document.querySelector(".navCloseBtn");

        navOpenBtn.addEventListener("click", () => {
            document.querySelector(".nav").classList.add("openNav");
        });

        navCloseBtn.addEventListener("click", () => {
            document.querySelector(".nav").classList.remove("openNav");
        });
      })
      .catch(error => console.error('Error loading navbar:', error));
});
