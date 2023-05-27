class ServerConnection {

    static methodType = Enum({ POST: 'POST', GET: 'GET'});

    data = new FormData();

    _request = new XMLHttpRequest();

    _postOnLoad = undefined;

    constructor(methodType, url) {
        const request = new XMLHttpRequest();
        request.open(methodType, url);

        request.onload = () => {
            let data;
            try {
                data = JSON.parse(request.responseText);
            } catch (e) {
                UserInfo.showUserInfoLink("Ошибка преобразования ответа сервера", "Ошибка преобразования ответа сервера", UserInfo.TypeInfo.Error, request.responseText)
                return;
            }

            if (data.UserMessage) {
                let typeUserMessage;
                if (data.UserMessageType == "Error") {
                    typeUserMessage = UserInfo.TypeInfo.Error;
                } else if (data.UserMessageType == "Success") {
                    typeUserMessage = UserInfo.TypeInfo.Success;
                } else if (data.UserMessageType == "Warning") {
                    typeUserMessage = UserInfo.TypeInfo.Warning;
                } else {
                    typeUserMessage = UserInfo.TypeInfo.Info;
                }

                UserInfo.showUserInfo(data.UserMessageTitle, data.UserMessageText, typeUserMessage);
                if (data.UserMessageType == "Error") {
                    return false;
                }
            }


            if (this._postOnLoad) {
                this._postOnLoad(data);
            }
        }
        this._request = request;
    }

    setOnLoad(onload) {
        this._postOnLoad = onload;
    }

    send() {
         this._request.send(this.data);
    }
}