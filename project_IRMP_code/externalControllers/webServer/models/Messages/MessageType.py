import enum


class MessageType(enum.Enum):
    info = "Info"
    success = "Success"
    warning = "Warning"
    error = "Error"
