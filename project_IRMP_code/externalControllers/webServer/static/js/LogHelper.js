let download_buttons = document.getElementsByName("download_log");
download_buttons.forEach(function(button) {
    button.onclick = function(){
        console.log("Скачивание файла лога");
        window.location.href = '/download_log/' + button.id;

        return false;
    }
});