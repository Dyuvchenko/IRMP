import os
from core import Core as Core2
from sqlalchemy.engine.base import Engine
from core.cameras.camController import CamerasController
from instruction import InstructionController

RootDerictory = os.path.dirname(os.path.abspath(__file__)) + "\\"
ConfigDict = {
    "launchMode": "production",
    "DataBase_logging": "False",
    "DataBaseLink": "sqlite:///db/dataBase/IRMP.db",
    "update_time_type": "sec",
    "update_time": "30"
}  # Перезаписывается при запуске

InitConfigLogging = False

InitConfigDict = False

DataBaseEngine: Engine = None

Core: Core2 = None

InstructionController: InstructionController = None

# возможны проблемы с порядком инициализации(
FlaskServerApp = None

# заполняется обязательным модулем cameras
CamController: CamerasController = CamerasController()  # на текущий момент из-за работы с камерами, не работает flask-debug,
# т.к. он перезапускает всё и при перезапуске оказывается, что камера уже занята(

# кладём суда имя модуля и имя метода
ModulesNamesBaseMethodsForUrl = dict()

# флаг аварийной остановки
emergency_stop = False

# флаг, дающий всем понять, что пора выключаться
stop_system = False
