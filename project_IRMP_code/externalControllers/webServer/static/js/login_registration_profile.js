document.addEventListener('DOMContentLoaded', () => {

    document.querySelector('#formLogin').onsubmit = () => {
        console.log("loginIn");

        let serverConnection = new ServerConnection(ServerConnection.methodType.POST, "/login");
        serverConnection.setOnLoad((data) => {
            if (data.success) {
                window.location.href = '/index';
//                document.querySelector('#loginInError').style.display = 'none';
            } else {
                document.querySelector('#loginInError').style.display = 'block';
            }
            return false;
        });
        serverConnection.data.append('userLogin', document.querySelector('#userNameLogin').value);
        serverConnection.data.append('userPassword', document.querySelector('#psw1Login').value);

        // Послать запрос
        serverConnection.send();
        return false;
    };

    document.querySelector('#formRegistration').onsubmit = () => {
        console.log("registration");

        let serverConnection = new ServerConnection(ServerConnection.methodType.POST, "/registration");
         serverConnection.setOnLoad((data) => {
            if (data.success) {
                window.location.href = '/index';
//                document.querySelector('#registrationError').style.display = 'none';
            } else {
                document.querySelector('#registrationError').style.display = 'block';
            }
            return false;
        });
        // Добавить данные для отправки с запросом
        serverConnection.data.append('userLogin', document.querySelector('#userNameRegistration').value);
        serverConnection.data.append('userPassword1', document.querySelector('#psw1Registration').value);
        serverConnection.data.append('userPassword2', document.querySelector('#psw2Registration').value);
        serverConnection.data.append('IRMPPIN', document.querySelector('#IRMPPIN').value);
        // Послать запрос
        serverConnection.send();
        return false;
    };

    document.querySelector('#logout').onclick = () => {
        console.log("logout");

        let serverConnection = new ServerConnection(ServerConnection.methodType.POST, "/logout");
        // Добавить данные для отправки с запросом
        serverConnection.data.append('logout', true);

        serverConnection.setOnLoad((data) => {
            if (data.success) {
//                window.location.href = '/index';
                window.location.reload();
            }
            return false;
        });
        // Послать запрос
        serverConnection.send();
        return false;
    };

});