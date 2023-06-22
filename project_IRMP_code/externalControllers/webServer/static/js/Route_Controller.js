if (document.querySelector("#add_route_btn") != null) {
    let button_added_route = document.querySelector("#add_route_btn");
    button_added_route.onclick = function() {
        console.log("Аварийная остановка");
        button_added_route.disabled = true;
        let serverConnection = new ServerConnection(ServerConnection.methodType.POST, "/adding_a_route");
        serverConnection.setOnLoad((data) => {
            if (data.success) {
                function reload_settings_page() {
                  window.location.href = '/map_info';
                }
                setTimeout(reload_settings_page, 3000);
            }
            return false;
        });
        serverConnection.send();
        return false;
    }
}


if (document.querySelector("#emergency_stop") != null) {
    let button_emergency_stop = document.querySelector("#emergency_stop");
    button_emergency_stop.onclick = function() {
        console.log("Остановка выполнения команды");
        button_emergency_stop.disabled = true;
        let serverConnection = new ServerConnection(ServerConnection.methodType.POST, "/emergency_stop");
        serverConnection.setOnLoad((data) => {
            button_emergency_stop.disabled = false;
            return false;
        });
        serverConnection.send();
        return false;
    }
}


if (document.querySelector("#stop_current_command") != null) {
    let button_stop_current_command = document.querySelector("#stop_current_command");
    button_stop_current_command.onclick = function() {
        console.log("Создание маршрута");
        button_stop_current_command.disabled = true;
        let serverConnection = new ServerConnection(ServerConnection.methodType.POST, "/stop_current_command");
        serverConnection.setOnLoad((data) => {
            button_stop_current_command.disabled = false;
            return false;
        });
        serverConnection.send();
        return false;
    }
}