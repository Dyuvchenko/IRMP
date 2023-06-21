let execute_command_buttons = document.getElementsByName("activate_command");
execute_command_buttons.forEach(function(button) {
    button.onclick = function(){
        console.log("Отправка команды (" + button.id + ") на выполнение");

        let serverConnection = new ServerConnection(ServerConnection.methodType.POST, "/execute_command");
        serverConnection.setOnLoad((data) => {

            return false;
        });
        serverConnection.data.append('command_name', button.id);
        serverConnection.send();

        return false;
    }
});