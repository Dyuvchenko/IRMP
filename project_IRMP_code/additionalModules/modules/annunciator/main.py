import logging

# подключаем файл с "blueprint"
import ProjectConsts
import socket
import additionalModules.modules.annunciator.annunciatorBlueperint
from additionalModules.modules.annunciator.annunciatorBlueperint import get_module_name
from additionalModules.modules.annunciator.annunciatorBlueperint import get_module_url_path
from core.ModuleSettings import ModuleSettings
from instruction.Instruction import Instruction

from additionalModules.modules.annunciator.annunciatorBlueperint import play_text


def update(emergency_stop):
    play_text()


def checking_ability_to_use_module():
    return True


module_settings = ModuleSettings(get_module_name(), not checking_ability_to_use_module(), checking_ability_to_use_module())
module_settings.url_path = get_module_url_path()

instructions = set()

instruction = Instruction()
instruction.name = "Проверка звука"


def sound_check():
    ProjectConsts.Core.voiceGuidanceController.play_sound(
        "Проверка звука. Если вы слышите данное сообщение, значит воспроизведение звука работает нормально")
    instruction.status_current_instruction = "Команда успешно выполнена"


instruction.function = sound_check

instructions.add(instruction)



# поиск своего ip)
instruction = Instruction()
instruction.name = "Адрес сайта"


def ip_check():
    message = "Ip адрес платформы: " + socket.gethostbyname(socket.gethostname()) + ". Порт: 8000"
    ProjectConsts.Core.voiceGuidanceController.play_sound(message)

    instruction.status_current_instruction = "Команда успешно выполнена"


instruction.function = ip_check

instructions.add(instruction)


def get_module_settings():
    return module_settings


def getModuleInstructions():
    return instructions
