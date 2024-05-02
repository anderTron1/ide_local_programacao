function blockCopy(e) {
    e.preventDefault();
    e.stopPropagation();
}

function blockPressCtrlC(e) {
    if (e.ctrlKey && e.keyCode == 67) {
        blockCopy(e);
    }
}

document.addEventListener("copy", blockCopy, false);
document.addEventListener("beforecopy", blockCopy, false);

document.addEventListener("keydown", blockPressCtrlC, false);

document.addEventListener('contextmenu', event => event.preventDefault());