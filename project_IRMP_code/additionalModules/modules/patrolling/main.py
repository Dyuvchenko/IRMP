import logging

# подключаем файл с "blueprint"
import additionalModules.modules.patrolling.PatrolBlueperint

from additionalModules.modules.patrolling.facial_req import show_facial_recognition


def update(emergency_stop):
    show_facial_recognition()


def checking_ability_to_use_module():
    return True
