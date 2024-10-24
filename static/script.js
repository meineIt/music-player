
document.querySelectorAll('.stars').forEach(function(starElement) {
    const starsNum = parseInt(starElement.getAttribute('data-stars'));
    starElement.innerHTML = '★'.repeat(starsNum);
})

function playSong(url) {
    console.log(url);
    const iframe = document.querySelector('.music-player-container iframe');
    iframe.src = url;
    document.getElementById('loadingText').style.display = 'none';
    document.getElementById('musicPlayerContainer').style.display = 'flex';
}


const lines = document.querySelectorAll('.text-line');
let currentIndex = 0;

function showNextLine() {
    if (currentIndex < lines.length) {
        lines[currentIndex].style.opacity = 1;
        currentIndex++;
        setTimeout(showNextLine, 500);
    }
}

window.onload = () => {
    showNextLine();
};