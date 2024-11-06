const phrases = ["Программирование (Python)", "Python+Майнкрафт", " Основы фронтенд-разработки",
    "Компьютерная грамотность", "Визуальное программирование", "Основы логики и программирования"];
let currentPhrase = 0;
let currentLetter = 0;
const typingAnimation = document.getElementById("typingAnimation");

function typePhrase() {
    if (currentLetter < phrases[currentPhrase].length) {
        typingAnimation.innerHTML += phrases[currentPhrase].charAt(currentLetter);
        currentLetter++;
        setTimeout(typePhrase, 100); // Adjust typing speed here
    } else {
        setTimeout(erasePhrase, 2000); // Wait before erasing
    }
}

function erasePhrase() {
    if (currentLetter > 0) {
        typingAnimation.innerHTML = phrases[currentPhrase].substring(0, currentLetter - 1);
        currentLetter--;
        setTimeout(erasePhrase, 50); // Adjust erasing speed here
    } else {
        currentPhrase = (currentPhrase + 1) % phrases.length;
        setTimeout(typePhrase, 500); // Wait before typing the next phrase
    }
}

document.addEventListener('DOMContentLoaded', (event) => {
    typePhrase(); // Start the typing animation
});