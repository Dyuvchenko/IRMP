
let disableButtons = document.getElementsByName("disable_module");
disableButtons.forEach(function(button) {
    button.onclick = function(){
        button.disabled = true;
        let module_path = button.id.split("_")[0];
        console.log("disable_module: " + module_path);

        let serverConnection = new ServerConnection(ServerConnection.methodType.POST, "/disable_module");
        serverConnection.setOnLoad((data) => {
            if (data.success) {
                function reload_settings_page() {
                  location.reload();
                }
                setTimeout(reload_settings_page, 3000);
            }
            return false;
        });
        serverConnection.data.append('module_path', module_path);

        // Послать запрос
        serverConnection.send();
        return false;
    }
});

let activateButtons = document.getElementsByName("activate_module");
activateButtons.forEach(function(button) {
    button.onclick = function(){
        button.disabled = true;
        let module_path = button.id.split("_")[0];
        console.log("activate_module: " + module_path);

        let serverConnection = new ServerConnection(ServerConnection.methodType.POST, "/activate_module");
        serverConnection.setOnLoad((data) => {
            if (data.success) {
                function reload_settings_page() {
                  location.reload();
                }
                setTimeout(reload_settings_page, 3000);
            }
            return false;
        });
        serverConnection.data.append('module_path', module_path);

        // Послать запрос
        serverConnection.send();
        return false;
    }
});

if (document.querySelector("#button_connect_to_wifi") != null) {
    let button_connect_to_wifi = document.querySelector("#button_connect_to_wifi");
    button_connect_to_wifi.onclick = function() {
        console.log("Попытка подключения к WIFI сети");
        button_connect_to_wifi.disabled = true;
        let serverConnection = new ServerConnection(ServerConnection.methodType.POST, "/connect_to_wifi");
        serverConnection.setOnLoad((data) => {
            if (data.success) {
                function reload_settings_page() {
                  location.reload();
                }
                setTimeout(reload_settings_page, 3000);
            }
            button_connect_to_wifi.disabled = false;
            return false;
        });
        serverConnection.data.append('wifi_ssid', document.querySelector("#inputWIFISSID").value);
        serverConnection.data.append('wifi_password', document.querySelector("#inputWIFIPASSWORD").value);

         function activate_button_wifi() {
             button_connect_to_wifi.disabled = false;
         }
         setTimeout(activate_button_wifi, 5000);
        // Послать запрос
        serverConnection.send();
        return false;
    }
}

if (document.querySelector("#update_module") != null) {
    let button_update_module = document.querySelector("#update_module");
    button_update_module.onclick = function() {
        console.log("Обновление статуса модулей");
        button_update_module.disabled = true;

         function update_module_timer() {
             button_update_module.disabled = false;
             location.reload();
         }
         setTimeout(update_module_timer, 5000);

        return false;
    }
}

if (document.querySelector("#update_system") != null) {
    let button_update_system = document.querySelector("#update_system");
    button_update_system.onclick = function() {
        console.log("Попытка обновления системы");
        button_update_system.disabled = true;
        let serverConnection = new ServerConnection(ServerConnection.methodType.POST, "/update_system");
        serverConnection.setOnLoad((data) => {
            button_update_system.disabled = false;
            return false;
        });

         function activate_button_update_system() {
             button_update_system.disabled = false;
         }
         setTimeout(activate_button_update_system, 5000);
        // Послать запрос
        serverConnection.send();
        return false;
    }
}