if (document.querySelector("#add_route_btn") != null) {
    let button_added_route = document.querySelector("#add_route_btn");
    button_added_route.onclick = function() {
        console.log("Создание маршрута");
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