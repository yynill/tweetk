function closeFlash(button) {
    // Find the parent flash div and remove it from the DOM
    var flashDiv = button.parentElement;
    flashDiv.remove();
}