import logging
import glob
import threading
import traceback

import ProjectConsts
from map.MapController import MapController
from instruction.InstructionController import InstructionController
from datetime import datetime
from core.ModuleSettings import ModuleSettings

"""Центральное ядро, через которое проходят все команды (по идее)"""


class Core:
    """ Контроллер карты"""
    __map_controller__: MapController = None

    """Логгер"""
    _logger_ = logging.getLogger()

    """ Основной поток core"""
    base_core_thread = None

    """Отключённые модули"""
    __disable_modules__ = set()

    """Мапа настроек модулей"""
    __modules_settings__ = dict()

    """Функции обновления модулей. Ключ - имя модуля, значение - функция"""
    functionsUpdateModule = dict()

    """Контроллер инструкций"""
    instructionController: InstructionController = None

    """Текущая инструкция на исполнении"""
    __current_instruction__ = None

    def __init__(self):
        self._logger_.info("Стар инициализации Core")
        self.instructionController = InstructionController()
        ProjectConsts.InstructionController = self.instructionController
        self.__config_disable_modules__()  # настраиваем отключённые модули
        self.__init_modules()  # инициализируем внешние модули
        self.__map_controller__ = MapController("58.102712, 38.621715")

        base_core_thread = threading.Thread(target=self.main_process)  # запускаем основной процесс core
        base_core_thread.start()

        update_core_thread = threading.Thread(target=self.update_process)  # запускаем процесс обновления модулей
        update_core_thread.start()
        self._logger_.info("Инициализации Core завершена")

    def __config_disable_modules__(self):
        self._logger_.info("Чтение файла с информацией об отключённых модулях...")
        with open("disable_modules.robo", "r") as configFile:  # открыть файл из рабочей директории в режиме чтения
            for line_setting in configFile.readlines():
                self.__disable_modules__.add(line_setting)
        self._logger_.info("Чтение файла с информацией об отключённых модулях завершено")

    def __init_modules(self):
        self._logger_.info("Стар инициализации внешних модулей")
        # Получаем все файлы с нужным расширением и в нужном месте
        main_py_modules = glob.glob("additionalModules/**/**/main.py")
        self._logger_.info("Запуск модулей:" + str(main_py_modules))
        module_settings: ModuleSettings = None  # сокращённое имя модуля (нормальное имя)
        for main_modul in main_py_modules:
            name_module = main_modul.replace("\\", ".") \
                .replace(".py", "")  # ну даже не имя модуля, а скорее путь к main файлу
            # получаем сокращённое имя модуля из main файлов модуля
            try:
                module_settings = __import__(name_module, globals(), locals(), ['update'], 0).get_module_settings()
                module_settings.path = name_module
                # добавляем модуль в список модулей
                self.__modules_settings__[module_settings.name] = module_settings
            except Exception:
                self._logger_.error("Ошибка получения настроек модуля:" + name_module)
                self._logger_.error(name_module + " не будет работать!")
                module_settings.error_init_module = True
                module_settings.is_disabled = True
                continue

            # если модуль есть в списке отключённых, тогда не инициализируем его
            if self.__disable_modules__.__contains__(name_module):
                module_settings.is_disabled = True
                continue
            try:
                __import__(name_module)  # первичный импорт main файлов модулей

                # импортируем функции update из main файлов модулей
                self.functionsUpdateModule[name_module] = \
                    __import__(name_module, globals(), locals(), ['update'], 0).update

            except ImportError:
                self._logger_.error("Ошибка инициализации модуля:" + name_module)
                self._logger_.error(name_module + " не будет работать!")
                module_settings.error_init_module = True
                module_settings.is_disabled = True

        self._logger_.info("Завершена инициализация внешних модулей")

    def main_process(self):
        logging.getLogger().info("main_process в core запущен")
        while True:
            if not ProjectConsts.emergency_stop: # пока не установлен флаг аварийной остановки
                self.processing_current_instructions()

            if ProjectConsts.stop_system: # пока не установлен флаг остановки системы
                break
        logging.getLogger().info("main_process в core завершил свою работу")

    # выполнение текущей инструкции
    def processing_current_instructions(self):
        self.__current_instruction__ = self.instructionController.get_current_instruction_or_none()
        if self.__current_instruction__: # если есть инструкция
            self.__current_instruction__()
            self.__current_instruction__ = None

    # процесс обновления модулей
    def update_process(self):
        logging.getLogger().info("update_process в core запущен")
        multiplier = None
        type = ProjectConsts.ConfigDict["update_time_type"]
        if type == "hour":
            # если часы, то умножаем на 60 (в минуты) и на 60 (в секунды)
            multiplier = 60 * 60
        if type == "min":
            # если минуты, то умножаем на 60
            multiplier = 60
        else:
            # иначе должны быть указаны секунды
            multiplier = 1
        time_now = Core.time_now_in_second()
        update_start_time = time_now
        time_pause = int(ProjectConsts.ConfigDict["update_time"]) * multiplier
        while True:
            time_now = Core.time_now_in_second()
            if time_now - time_pause > update_start_time: # запускаем обновление по таймеру
                update_start_time = time_now
                self._logger_.info("Запущено обновление модулей")
                self.update_module()
                self._logger_.info("Обновление модулей завершено")

            if ProjectConsts.stop_system:
                break
        logging.getLogger().info("update_process в core завершил свою работу")

    # обновление модулей
    def update_module(self):
        for name_module, functionUpdate in self.functionsUpdateModule.items():
            if self.__disable_modules__.__contains__(name_module):
                continue
            try:
                self._logger_.info("Обновление модуля: " + name_module)
                functionUpdate(ProjectConsts.emergency_stop)
            except Exception:
                self._logger_.error("Ошибка при выполнении update() в модуле:" + name_module)
                self._logger_.error(traceback.format_exc())

    """Получаем текущее время с переводом в секунды"""
    @staticmethod
    def time_now_in_second():
        return datetime.now().time().second + datetime.now().time().minute * 60 + datetime.now().time().hour * 60 * 60

    """Получить настройки модулей"""
    def get_modules_settings(self):
        return self.__modules_settings__

    """Получить отключённые модули"""
    def get_disable_modules(self):
        return self.__disable_modules__
