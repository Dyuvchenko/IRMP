import os
from glob import glob
from time import sleep

import cv2
from flask import Blueprint, url_for, Response, render_template, request
from flask.json import jsonify
from flask_login import login_required

import ProjectConsts
import additionalModules.modules.patrolling.main
from additionalModules.modules.patrolling.train_model import train_model
from externalControllers.webServer.FlaskHelper import FlaskHelper
from externalControllers.webServer.models.Messages.MessageType import MessageType
from externalControllers.webServer.models.Messages.UserMessage import UserMessage

name = "annunciatior"
templates_path = os.path.dirname(os.path.realpath(__file__)) + "\\templates"
annunciatior = Blueprint(name, __name__, template_folder=templates_path)

flaskHelper = FlaskHelper()
modulePath = os.getcwd() + "\\additionalModules\\modules\\annunciatior\\"


# templates_path = os.path.dirname(os.path.realpath(__file__)) + "\\templates"


def base_render_template(template_name_or_list, **context):
    return flaskHelper.base_render_template(template_name_or_list, **context)


text_for_play = ""


def set_text(text):
    global text_for_play
    text_for_play = text


def play_text():
    global text_for_play
    if text_for_play == "":
        return
    ProjectConsts.Core.voiceGuidanceController.play_sound(text_for_play)


@annunciatior.route("/index", methods=["GET"])
@annunciatior.route('/')
@login_required
def annunciatior_index():
    return base_render_template("annuciatior.html")


@annunciatior.route("/update_message", methods=["POST"])
def update_message():
    response_data = {}

    response_data['success'] = True
    new_message = request.form['new_message']
    global text_for_play
    text_for_play = new_message
    UserMessage("Обновление оповещения", MessageType.success,
                "Обновление оповещения выполнено успешно.").add_from_response_data(response_data)
    return jsonify(response_data)


def get_module_name():
    return "Оповещатель"


def get_module_url_path():
    return name + "." + annunciatior_index.__name__


flaskHelper.register_blueprint(annunciatior, name)
