document.getElementById("toggle-menu").addEventListener("click", function(event) {
    event.stopPropagation(); // Evitar que el clic se propague al documento
    const dropdown = document.getElementById("dropdown");
    const arrow = this;

    // Cambia la visibilidad del menú
    dropdown.style.display = dropdown.style.display === "block" ? "none" : "block";
    
    // Rota la flecha
    arrow.classList.toggle("rotate");
});

// Cerrar el menú si se hace clic fuera de él
window.onclick = function(event) {
    const dropdown = document.getElementById("dropdown");
    const arrow = document.getElementById("toggle-menu");
    
    if (dropdown.style.display === 'block' && !event.target.matches('#toggle-menu')) {
        dropdown.style.display = 'none'; // Oculta el menú si se hace clic fuera
        arrow.classList.remove("rotate"); // Restaura la posición de la flecha
    }
};
