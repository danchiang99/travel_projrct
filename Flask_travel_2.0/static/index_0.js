const images = ['static/img/background-03.jpg', 'static/img/background-04.jpg' ,'static/img/background-05.jpg','static/img/background-06.jpg','static/img/background-07.jpg'];
let currentIndex = 0;

function changeBackground() {
    const bgImage = document.querySelector('.fullscreen-bg img');
    bgImage.style.opacity = 0;

    setTimeout(() => {
        currentIndex = (currentIndex + 1) % images.length;
        const newImage = new Image();
        newImage.src = images[currentIndex];
        newImage.onload = function() {
            bgImage.src = this.src;
            bgImage.style.opacity = 1;
        };
    }, 900);
}


window.onload = function() {
    changeBackground();

    setInterval(changeBackground, 8000);
};