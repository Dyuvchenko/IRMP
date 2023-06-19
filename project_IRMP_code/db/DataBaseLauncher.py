import glob
import logging

from sqlalchemy import create_engine

import ProjectConsts
from db.DataBaseObject import DataBaseObject
import map.models


class DataBaseLauncher:
    @staticmethod
    def init_data_base():
        logging.getLogger().info("Старт инициализации базы данных.")
        DataBaseLauncher.create_data_base_core()
        logging.getLogger().info("Старт генерации метаданных для работы базы данных.")
        DataBaseLauncher.create_metadata()
        logging.getLogger().info("Генерация метаданных завершена.")
        logging.getLogger().info("База данных инициализирована.")

    """создание ядра"""
    @staticmethod
    def create_data_base_core():
        if ProjectConsts.ConfigDict.get("DataBase_logging") == "True":
            engine = create_engine(ProjectConsts.ConfigDict.get("DataBaseLink"), echo=True)
        else:
            engine = create_engine(ProjectConsts.ConfigDict.get("DataBaseLink"))
        ProjectConsts.DataBaseEngine = engine

    @staticmethod
    def create_metadata():
        # создаем таблиц
        DataBaseObject.metadata.create_all(bind=ProjectConsts.DataBaseEngine)

    @staticmethod
    def __include__modules__for__create__metadata_models():
        logging.getLogger().info("Стар поиска и подключения моделей БД внешних модулей")
        # Получаем все файлы с нужным расширением и в нужном месте
        modules_py_modules = glob.glob("additionalModules/**/**/models.py")
        logging.getLogger().info("Подключение моделей модулей:" + str(modules_py_modules))
        for model_modul in modules_py_modules:
            name_model_module = model_modul.replace("\\", ".").replace(".py","")
            try:
                __import__(name_model_module)
            except ImportError:
                logging.getLogger().error("Ошибка инициализации модуля:" + name_model_module)
                logging.getLogger().error(name_model_module + " не будет работать!")
            # exec(open(main_modul).read())
        # print(glob.glob("../additionalModules/modules/main.py"))
        logging.getLogger().info("Завершена инициализация внешних модулей")
