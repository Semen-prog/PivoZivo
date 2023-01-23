function onClickSettings() {
    element = document.getElementById("drop-list");
    const vis = element.style.visibility;
    if (vis == "visible") {
        element.style.visibility = 'hidden';
    }
    else {
        element.style.visibility = 'visible';
    }
}