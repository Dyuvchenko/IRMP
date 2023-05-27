class Cam_helper {

    start_video_feed() {
        console.log("start_video_feed");

        let serverConnection = new ServerConnection(ServerConnection.methodType.POST, URL_Helper.getBaseUrl() + "/update_video_feed");
        serverConnection.data.append('video_feed', true);
        serverConnection.data.append('data', 'asdasdasdasdasddddddddddddddddddddddddddddddddddddddddddddddddddd');

        // Послать запрос
        serverConnection.send();
        return false;
    }

    stop_video_feed() {
        console.log("stop_video_feed");

        let serverConnection = new ServerConnection(ServerConnection.methodType.POST, URL_Helper.getBaseUrl() + "/update_video_feed");
        serverConnection.data.append('video_feed', false);
        serverConnection.data.append('data', 'asdasdasdasdasddddddddddddddddddddddddddddddddddddddddddddddddddd');

        serverConnection.setOnLoad((data) => {
            if (data.success) {
                window.location.href = '/index';
//                document.querySelector('#registrationError').style.display = 'none';
            } else {
                document.querySelector('#registrationError').style.display = 'block';
            }
            return false;
        });

        // Послать запрос
        serverConnection.send();
        return false;
    }
}