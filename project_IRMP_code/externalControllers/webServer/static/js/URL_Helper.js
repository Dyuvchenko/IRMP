class URL_Helper {
    static need_reload = false

    static getBaseUrl() {
        return window.location.href.substring(0,window.location.href.indexOf("/",8));
    }

    static reloadStream() {
      document.getElementById("patrol_video_feed").src =
          document.getElementById("patrol_video_feed").src.split("?")[0] + "?ver=" + new Date().getTime();
    }

    static autoReloadStream() {
        if (URL_Helper.need_reload) {
            URL_Helper.reloadStream();
            setTimeout(URL_Helper.autoReloadStream, 900); // в миллисекундах
        }
    }
}