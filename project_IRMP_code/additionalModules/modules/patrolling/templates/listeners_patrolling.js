// есть проблема, что пока flask выдаёт strem video, то не принимает другеи запросы (т.е. видео не остановить)
// поэтому, видео передаётся только какой-то промежуток времени, а потом мы его перезапускаем

$( "#add_new_people_patrolling" ).on('show.bs.modal', function(){
    console.log("openModal");
    URL_Helper.need_reload = true;
    URL_Helper.autoReloadStream();
});
$( "#add_new_people_patrolling" ).on('hide.bs.modal', function(){
    URL_Helper.need_reload = false;
    console.log("openHidden");
});

take_photo.onclick = function() {
    console.log("take_photo");
    take_photo.disabled = true
    let serverConnection = new ServerConnection(ServerConnection.methodType.POST, "/patrol/take_photo");
    serverConnection.setOnLoad((data) => {
        take_photo.disabled = false
        if (data.count_photo) {
            document.getElementById("take_photo_count").innerHTML = "Осталось : " + data.count_photo;
        }
        if (data.photo_success){
            window.location.href = '/patrol/people';
        }
        return false;
    });
    serverConnection.data.append('take_photo', 'take_photo');
    serverConnection.data.append('name_people', document.getElementById("input_name").value);

    // Послать запрос
    serverConnection.send();
    return false;
};


// Выбираем все кнопки на странице и получаем массив
var buttons = document.getElementsByClassName('btn-delete-people-recognizer')
// Проходим по массиву
for (let button of buttons) {
  // Вешаем событие клик
  button.addEventListener('click', function(e) {
    console.log(button.id);
    button.disabled = true
    let serverConnection = new ServerConnection(ServerConnection.methodType.POST, "/patrol/delete_people");
    serverConnection.setOnLoad((data) => {
        button.disabled = false
        if (data.photo_success){
            document.getElementById("li_" + button.id).remove();
        }
        return false;
    });
    serverConnection.data.append('name_people', button.id.split("=")[1]);

    // Послать запрос
    serverConnection.send();
    return false;
  })
}