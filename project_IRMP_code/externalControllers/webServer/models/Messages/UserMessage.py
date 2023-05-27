from externalControllers.webServer.models.Messages.MessageType import MessageType


class UserMessage:
    def __init__(self):
        self.__type = MessageType.info
        self.__message = "Справочная информация"
        self.__title = "Информация"

    def __init__(self, title, message_type, message):
        self.__type = message_type
        self.__message = message
        self.__title = title

    def get_type(self):
        return self.__type

    def get_messages(self):
        return self.__type

    def add_from_response_data(self, response_data):
        response_data["UserMessage"] = "True"
        response_data["UserMessageTitle"] = self.__title
        response_data["UserMessageType"] = self.__type.value
        response_data["UserMessageText"] = self.__message

