import datetime
import logging
import os
import sys

from core.Core import Core
from db.DataBaseLauncher import DataBaseLauncher
from externalControllers.webServer.main import launch_server_debug, launch_server_production

import ProjectConsts


# настраиваем логирование
def config_logging(logger):
    logger.setLevel(logging.DEBUG)

    if ProjectConsts.ConfigDict.get("launchMode") == "debug":
        console_handler = logging.StreamHandler(sys.stdout)
        logging.basicConfig(handlers=[console_handler],
                            format="%(name)s - %(levelname)s - %(asctime)s - %(message)s")
    else:
        default_logging_file = ProjectConsts.RootDerictory + "logs\\robo_log.log"
        if os.path.exists(default_logging_file):  # если существует файл лога, то переименуем его
            data_time_str = datetime.datetime.now().strftime("%m.%d.%Y_%H-%M-%S")
            logging_file = ProjectConsts.RootDerictory + "logs\\" + data_time_str + "_robo_log.log"
            number_launch = 1
            while os.path.exists(logging_file):  # подбираем номер запуска, которого ещё не было
                # обрезаем .log и убираем номер запуска
                logging_file = logging_file[:-4].split("#")[0] + "#launch-" + str(number_launch) + ".log"
                number_launch += 1
            os.rename(default_logging_file, logging_file)
        # создаём хендлер для файла лога, кодировка файла будет UTF-8 для поддержки кириллических сообщений в логе
        file_handler = logging.FileHandler(filename=default_logging_file, encoding="utf-8")
        # создаём хендлер для консоли
        console_handler = logging.StreamHandler(sys.stdout)
        logging.basicConfig(handlers=[file_handler, console_handler],
                            format="%(name)s - %(levelname)s - %(asctime)s - %(message)s")
    ProjectConsts.InitConfigLogging = True


# читаем конфигурацию из файла
def reading_configuration_from_file(logger):
    logger.info("Чтение конфигурации из файла...")
    config_dict = {}
    with open("config.robo", "r") as configFile:  # открыть файл из рабочей директории в режиме чтения
        for line_setting in configFile.readlines():
            setting, char, value = line_setting.split()[:3]
            config_dict[setting] = value
    ProjectConsts.ConfigDict.update(config_dict)
    ProjectConsts.InitConfigDict = True
    logger.info("Чтение конфигурации из файла завершено")


# точка старта
if __name__ == "__main__":

    # os.chdir("/home/modex/Desktop/IRMP/project_IRMP_code/")

    if not ProjectConsts.InitConfigDict:
        reading_configuration_from_file(logging.getLogger())

    if not ProjectConsts.InitConfigLogging:
        config_logging(logging.getLogger())

    # запускаем БД
    DataBaseLauncher.init_data_base()

    # запускаем ядро
    ProjectConsts.Core = Core()

    # ProjectConsts.Core.voiceGuidanceController.play_sound("Система успешно запущена, производится запуск сайта.")

    # запускаем сайт
    if ProjectConsts.ConfigDict.get("launchMode") == "debug":
        launch_server_debug()
    else:
        launch_server_production()
