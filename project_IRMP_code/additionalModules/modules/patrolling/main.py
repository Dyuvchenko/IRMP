import logging

# подключаем файл с "blueprint"
import additionalModules.modules.patrolling.PatrolBlueperint
from additionalModules.modules.patrolling.PatrolBlueperint import get_module_name
from additionalModules.modules.patrolling.PatrolBlueperint import get_module_url_path
from core.ModuleSettings import ModuleSettings

from additionalModules.modules.patrolling.facial_req import show_facial_recognition


def update(emergency_stop):
    show_facial_recognition()


def checking_ability_to_use_module():
    return True


module_settings = ModuleSettings(get_module_name(), not checking_ability_to_use_module(), checking_ability_to_use_module())
module_settings.url_path = get_module_url_path()


def get_module_settings():
    return module_settings
