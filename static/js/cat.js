const cat = document.getElementById('cat');

function moveCat() {
    const windowWidth = window.innerWidth;
    const windowHeight = window.innerHeight;

    const randomX = Math.random() * (windowWidth - 100);
    const randomY = Math.random() * (windowHeight - 100);

    cat.style.left = `${randomX}px`;
    cat.style.top = `${randomY}px`;
}

setInterval(moveCat, 2000);


cat.addEventListener('click', function() {
    window.location.href = 'https://www.youtube.com/watch?v=2UsTvXvdFcs';
});
