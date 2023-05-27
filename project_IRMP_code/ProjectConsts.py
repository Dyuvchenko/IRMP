import os
from core import Core
from sqlalchemy.engine.base import Engine
from core.cameras.camController import CamerasController

RootDerictory = os.path.dirname(os.path.abspath(__file__)) + "\\"
ConfigDict = {
    "launchMode": "production",
    "DataBase_logging": "False",
    "DataBaseLink": "sqlite:///db/dataBase/IRMP.db"
}  # Перезаписывается при запуске

InitConfigLogging = False

InitConfigDict = False

DataBaseEngine: Engine = None

Core: Core = None

# возможны проблемы с порядком инициализации(
FlaskServerApp = None

# заполняется обязательным модулем cameras
CamController: CamerasController = CamerasController()  # на текущий момент из-за работы с камерами, не работает flask-debug,
# т.к. он перезапускает всё и при перезапуске оказывается, что камера уже занята(

# кладём суда имя модуля и имя метода
ModulesNamesBaseMethodsForUrl = dict()


# флаг, дающий всем понять, что пора выключаться
stop_system = False
