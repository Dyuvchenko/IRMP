import logging
import glob
import threading

import ProjectConsts
from map.MapController import MapController

"""Центральное ядро, через которое проходят все команды (по идее)"""


class Core:
    __map_controller__: MapController = None
    _logger_ = logging.getLogger()

    base_core_thread = None

    functionsUpdateModule = dict()

    instructions = []

    def __init__(self):
        self._logger_.info("Стар инициализации Core")
        self.__map_controller__ = MapController("58.102712, 38.621715")  # TODO получение данных с arduino!
        self.__init_modules()
        self._logger_.info("Инициализации Core завершена")


        # base_core_thread = threading.Thread(target=self.main_process)
        # base_core_thread.start()

    def __init_modules(self):
        self._logger_.info("Стар инициализации внешних модулей")
        # Получаем все файлы с нужным расширением и в нужном месте
        main_py_modules = glob.glob("additionalModules/**/**/main.py")
        self._logger_.info("Запуск модулей:" + str(main_py_modules))
        for main_modul in main_py_modules:
            name_module = main_modul.replace("\\", ".").replace(".py", "")
            try:
                # from additionalModules.modules.patrolling.main import update
                __import__(name_module)  # первичный импорт main файлов модулей

                # импортируем функции update из main файлов модулей
                self.functionsUpdateModule[name_module] = \
                    __import__(name_module, globals(), locals(), ['update'], 0).update

            except ImportError:
                self._logger_.error("Ошибка инициализации модуля:" + name_module)
                self._logger_.error(name_module + " не будет работать!")
            # exec(open(main_modul).read())
        # print(glob.glob("../additionalModules/modules/main.py"))
        self._logger_.info("Завершена инициализация внешних модулей")

    def main_process(self):
        logging.getLogger().info("main_process в core запущен")
        while True:

            for name_module, functionUpdate in self.functionsUpdateModule.items():
                try:
                    functionUpdate()
                except Exception:
                    self._logger_.error("Ошибка при выполнении update() в модуле:" + name_module)
            if ProjectConsts.stop_system:
                break
        logging.getLogger().info("main_process в core завершил свою работу")
