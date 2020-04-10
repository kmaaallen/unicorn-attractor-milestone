// function to display confirm modal
confirmModal = function (text, url) {
    // shade out background
    var overlay = document.getElementsByClassName("overlay")[0];
    overlay.style.display = "block";
    // get modal to display
    var modal = document.getElementById("confirmModal");
    // get p tag to display passed in message
    var message = document.getElementById("confirmText");
    // set confirm message from passed in text
    message.innerHTML = text;
    // show modal
    modal.style.display = "block";
    // get confirm button
    var confirmButton = document.getElementById("confirmButton");
    confirmButton.setAttribute("href", url);
}

closeModal = function () {
    // unshade out background
    var overlay = document.getElementsByClassName("overlay")[0];
    overlay.style.display = "none";
    // close modal
    document.getElementById("confirmModal").style.display = "none";
    
}