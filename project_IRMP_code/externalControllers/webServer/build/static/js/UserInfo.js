class UserInfo {
    static newWin;

    static TypeInfo = Enum({ Info: 'Info', Warning: 'Warning', Error: "Error", Success: "Success"});

    static showUserInfoLink(textHeader, textInfo, typeInfo, textForBlank) {
        document.querySelector('#userInfoModalTitle').textContent = textHeader;
        switch(typeInfo)
        {
            case UserInfo.TypeInfo.Success:
                document.querySelector('#userMessageInfoData').classList.value = "alert alert-success";
                break;

            case UserInfo.TypeInfo.Info:
                document.querySelector('#userMessageInfoData').classList.value = "alert alert-info";
                break;

            case UserInfo.TypeInfo.Warning:
                document.querySelector('#userMessageInfoData').classList.value = "alert alert-warning";
                break;

            case UserInfo.TypeInfo.Error:
                document.querySelector('#userMessageInfoData').classList.value = "alert alert-danger";
                break;

            default:
                document.querySelector('#userMessageInfoData').classList.value = "alert alert-info";
        }
        document.querySelector('#userMessageInfoData').textContent = textInfo;
        UserInfo.addUserInfoButtonLink(textHeader, textForBlank, typeInfo);
        $("#userInfo").modal('show');
    }

    static showUserInfo(textHeader, textInfo, typeInfo) {
        document.querySelector('#userInfoModalTitle').textContent = textHeader;
        switch(typeInfo)
        {
            case UserInfo.TypeInfo.Success:
                document.querySelector('#userMessageInfoData').classList.value = "alert alert-success";
                break;

            case UserInfo.TypeInfo.Info:
                document.querySelector('#userMessageInfoData').classList.value = "alert alert-info";
                break;

            case UserInfo.TypeInfo.Warning:
                document.querySelector('#userMessageInfoData').classList.value = "alert alert-warning";
                break;

            case UserInfo.TypeInfo.Error:
                document.querySelector('#userMessageInfoData').classList.value = "alert alert-danger";
                break;

            default:
                document.querySelector('#userMessageInfoData').classList.value = "alert alert-info";
        }
        document.querySelector('#userMessageInfoData').textContent = textInfo;
        $("#userInfo").modal('show');
    }

    static addUserInfoButtonLink(nameBlankUrl, text, typeInfo) {
        let classButton;
        switch(typeInfo)
        {
            case UserInfo.TypeInfo.Success:
                classButton = "alert-success";
                break;

            case UserInfo.TypeInfo.Info:
                classButton = "alert-info";
                break;

            case UserInfo.TypeInfo.Warning:
                classButton = "alert-warning";
                break;

            case UserInfo.TypeInfo.Error:
                classButton = "alert-danger";
                break;

            default:
                classButton = "alert-info";
        }

        let button = document.createElement('button');
        button.className = "alert " + classButton;
        button.innerHTML = "Нажмите, чтобы просмотреть дополнительную информацию";
        button.style = "margin-top: 10px";
        button.onclick = function () {
            if (UserInfo.newWin) {
                UserInfo.newWin.close();
            }
            UserInfo.newWin = window.open("about:blank", "Info");
            UserInfo.newWin.document.write(text);
        }

        document.querySelector('#userMessageInfoData').append(button);
    }
}