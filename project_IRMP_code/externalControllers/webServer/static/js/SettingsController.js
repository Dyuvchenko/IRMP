if(document.querySelector("#disable_module")) {
    document.querySelector("#disable_module").onclick = function(){
        document.querySelector("#disable_module").disabled = true;
        let module_path = document.querySelector("#disable_module").name;
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
}
if(document.querySelector("#activate_module")) {
    document.querySelector("#activate_module").onclick = function(){
        document.querySelector("#activate_module").disabled = true;
        let module_path = document.querySelector("#activate_module").name;
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
}