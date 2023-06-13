import os
from glob import glob
from time import sleep

import cv2
from flask import Blueprint, url_for, Response, render_template, request
from flask.json import jsonify

import ProjectConsts
import additionalModules.modules.patrolling.main
from additionalModules.modules.patrolling.train_model import train_model
from externalControllers.webServer.FlaskHelper import FlaskHelper
from externalControllers.webServer.models.Messages.MessageType import MessageType
from externalControllers.webServer.models.Messages.UserMessage import UserMessage

name = "patrol"
templates_path = os.path.dirname(os.path.realpath(__file__)) + "\\templates"
patrol = Blueprint(name, __name__, template_folder=templates_path)

flaskHelper = FlaskHelper()
modulePath = os.getcwd() + "\\additionalModules\\modules\\patrolling\\"


# templates_path = os.path.dirname(os.path.realpath(__file__)) + "\\templates"


def base_render_template(template_name_or_list, **context):
    return flaskHelper.base_render_template(template_name_or_list, users_recognition=get_users(), **context)


@patrol.route("/index", methods=["GET"])
@patrol.route('/')
def patrol_index():
    return base_render_template("patrol.html")


@patrol.route('/people')
def patrol_people():
    return base_render_template("facial_recognition.html")


@patrol.route("/listeners_patrolling")
def listeners_patrolling():
    return render_template("listeners_patrolling.js")


@patrol.route("/delete_people", methods=["POST"])
def delete_people():
    response_data = {}
    name_people = request.form["name_people"]
    people_path = modulePath + "dataset\\" + name_people
    for file in glob(people_path + '\\image' + '*.jpg'):
        os.remove(file)
    os.removedirs(people_path)
    train_model()
    UserMessage("Удаление человека выполнено успешно!", MessageType.success, "Удаление человека выполнено успешно!") \
        .add_from_response_data(response_data)
    response_data["photo_success"] = True
    return jsonify(response_data)


@patrol.route("/take_photo", methods=["POST"])
def take_photo():
    response_data = {}
    take_photo = request.form["take_photo"]
    name_people = request.form["name_people"]

    people_path = modulePath + "dataset\\" + name_people
    if take_photo != "":
        if name_people != "":
            # если нету такого пользователя, то создаём его
            if not os.path.exists(people_path):
                os.mkdir(people_path)
            # считаем сколько есть
            count_img = len(glob(people_path + '\\image' + '*.jpg'))
            response_data["count_photo"] = 9 - count_img

            # делаем фото)
            img_name = people_path + "\\image_{}.jpg".format(count_img)
            cv2.imwrite(img_name, ProjectConsts.CamController.camera.get_frame(_bytes=False))
            count_img += 1

            if count_img > 9:
                response_data["photo_success"] = True
                train_model()
                UserMessage("Обучение распознавания новому человеку завершено!", MessageType.success,
                            "Обучение распознавания новому человеку завершено!") \
                    .add_from_response_data(response_data)
            else:
                UserMessage("Фотография успешно сделана", MessageType.success, "Фотография успешно сделана") \
                    .add_from_response_data(response_data)

        else:
            UserMessage("Ошибка добавления пользователя", MessageType.error, "Не указано ФИО нового человека") \
                .add_from_response_data(response_data)

    return jsonify(response_data)


def get_users():
    return os.listdir(modulePath + "dataset\\")


def get_module_name():
    return "Патрулирование"


def get_module_url_path():
    return name + "." + patrol_index.__name__


flaskHelper.register_blueprint(patrol, name)
