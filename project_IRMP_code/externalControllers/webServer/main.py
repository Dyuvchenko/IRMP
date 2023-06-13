import logging
import os.path
import sys
from time import sleep

from flask import Flask, render_template, g, request, flash, session, jsonify, Response
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_flatpages import FlatPages
from flask_frozen import Freezer
import folium
from sqlalchemy.orm import Session

import ProjectConsts
from externalControllers.webServer.FlaskHelper import FlaskHelper
from externalControllers.webServer.FoliumMapHelper import FoliumMapHelper
from externalControllers.webServer.RoutePointOnMap import RoutePointOnMap
from externalControllers.webServer.models.UserLogin import UserLogin
from werkzeug.security import generate_password_hash, check_password_hash
from externalControllers.webServer.models.Messages.UserMessage import UserMessage
from externalControllers.webServer.models.Messages.MessageType import MessageType

logger = logging.getLogger()

DEBUG = True
SECRET_KEY = 'fdgfh78@#5?>gfhf89dx,v06k'  # Сделать генерацию ключа
# FLATPAGES_AUTO_RELOAD = DEBUG
# FLATPAGES_EXTENSION = '.md'
# FLATPAGES_ROOT = 'content'
# POST_DIR = 'posts'

app = Flask(__name__)
ProjectConsts.FlaskServerApp = app
flatpages = FlatPages(app)
freezer = Freezer(app)
app.config.from_object(__name__)
# app.config["SECRET_KEY"] = "asdawdcffsrfg342r4tg5r6u7"  #TODO Сделать генерацию ключа

login_manager = LoginManager(app)
login_manager.login_view = 'need_login'

# login_manager.login_message = "Авторизуйтесь для доступа к закрытым страницам"
# login_manager.login_message_category = "success"

flaskHelper = FlaskHelper()


def base_render_template(template_name_or_list, **context):
    return flaskHelper.base_render_template(template_name_or_list, **context)


@login_manager.user_loader
def load_user(user_id):
    user = UserLogin.fromDB(user_id, g.__db)
    logger.info("Осуществлён вход пользователем: " + user.login)
    return user


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    response_data = {}
    if request.form['logout']:
        current_user.logout()
        logout_user()
        UserMessage("Выход из аккаунта", MessageType.success, "Вы успешно вышли из аккаунта") \
            .add_from_response_data(response_data)
        response_data['success'] = True
        print("logout")
    return jsonify(response_data)


@app.route("/login", methods=["POST"])
def login():
    response_data = {}
    if not request.form['userLogin']:
        UserMessage("Ошибка входа", MessageType.error, "Не указан логин пользователя") \
            .add_from_response_data(response_data)
    else:
        user = g.__db.query(UserLogin).filter(UserLogin.login == request.form['userLogin']).first()
        # user = g.__db.getUserByLogin(request.form['userLogin'])
        if user and check_password_hash(user.password, request.form['userPassword']):
            # user_login = UserLogin().create(user)
            # login_user(user_login)
            login_user(user)
            response_data['success'] = True
        else:
            UserMessage("Ошибка входа", MessageType.error, "Неверная пара логин/пароль") \
                .add_from_response_data(response_data)
    return jsonify(response_data)


IRMPPIN = "1-1-1-1"


@app.route("/registration", methods=["POST"])
def registration():
    response_data = {}

    user_login = request.form['userLogin']
    if not user_login:
        UserMessage("Ошибка", MessageType.error, "Логин не задан!").add_from_response_data(response_data=response_data)
    else:
        if g.__db.query(UserLogin).filter(UserLogin.login == request.form['userLogin']).first():
            UserMessage("Ошибка", MessageType.error, "Такой пользователь уже существует!") \
                .add_from_response_data(response_data=response_data)
        else:
            user_password1 = request.form['userPassword1']
            user_password2 = request.form['userPassword2']
            if user_password1 != user_password2:
                UserMessage("Ошибка", MessageType.error, "Пароли не совпадают!") \
                    .add_from_response_data(response_data=response_data)
            else:
                user_IRMPPIN = request.form['IRMPPIN']

                if user_IRMPPIN != IRMPPIN:
                    UserMessage("Ошибка", MessageType.error, "Уникальный PIN платформы указан не верно!") \
                        .add_from_response_data(response_data=response_data)
                else:
                    newUser = UserLogin(login=user_login, password=generate_password_hash(user_password1))
                    g.__db.add(newUser)  # добавляем в бд
                    g.__db.commit()  # сохраняем изменения
                    # db.refresh(newUser)  # обновляем состояние объекта
                    response_data['success'] = True
                    login_user(newUser)

                    # g.__db.query(UserLogin).filter(UserLogin.login == request.form['userLogin']).first()
                    # if g.__db.addUser(user_login, generate_password_hash(user_password1)):
                    #     response_data['success'] = True
                    #     user = g.__db.getUserByLogin(user_login)
                    #     user_login = UserLogin().create(user)
                    #     login_user(user_login)
    return jsonify(response_data)


@app.before_request
def before_request():
    """Установление соединения с БД перед выполнением запроса"""
    g.__db = Session(autoflush=False, bind=ProjectConsts.DataBaseEngine)
    # g.__db = DataBaseExecutor(DataBaseHelper.get_db(g, app))


@app.teardown_appcontext
def close_db(error):
    """Закрываем соединение с БД, если оно было установлено"""
    if g.__db:
        g.__db.commit()  # сохраняем изменения
        g.__db.close()
    # if hasattr(g, 'link_db'):
    #     g.link_db.close()


@app.route("/index", methods=["GET"])
@app.route("/", methods=["GET"])
def index():
    flash("Имя пользователя больше 2", category="success")
    return base_render_template("index.html")


@app.route("/test", methods=["GET"])
def test():
    return render_template("test.html")


@app.route("/settings", methods=["GET"])
def settings():
    return base_render_template(
        "settings.html",
        modules=ProjectConsts.Core.get_modules_settings()
    )


@app.route("/activate_module", methods=["POST"])
def activate_module():
    module_path = request.form['module_path']
    response_data = {}
    for name_module, module_settings in ProjectConsts.Core.get_modules_settings().items():
        if module_settings.path == module_path:
            module_settings.is_disabled = False
            response_data['success'] = True

            # читаем файл и записываем новый, обновлённый конфиг файл
            update_config_disable_modules_file(activate_module_path=module_path, disable_module_path=None)
            # записываем обновлённые отключённые модули

            UserMessage("Активация модуля", MessageType.success, "Модуль '" + name_module + "' успешно активирован") \
                .add_from_response_data(response_data)
            break
    return jsonify(response_data)


@app.route("/disable_module", methods=["POST"])
def disable_module():
    module_path = request.form['module_path']
    response_data = {}
    for name_module, module_settings in ProjectConsts.Core.get_modules_settings().items():
        if module_settings.path == module_path:
            module_settings.is_disabled = True
            response_data['success'] = True

            # читаем файл и записываем новый, обновлённый конфиг файл
            update_config_disable_modules_file(activate_module_path=None, disable_module_path=module_path)
            # записываем обновлённые отключённые модули

            UserMessage("Деактивация модуля", MessageType.success,
                        "Модуль '" + name_module + "' успешно деактивирован").add_from_response_data(response_data)
            break
    return jsonify(response_data)


def update_config_disable_modules_file(activate_module_path, disable_module_path):
    disable_modules = set()
    with open("disable_modules.robo", "r") as configFile:  # открыть файл из рабочей директории в режиме чтения
        for line_setting in configFile.readlines():
            if line_setting == activate_module_path:
                continue
            else:
                disable_modules.add(line_setting)
    # if activate_module_path:
    if disable_module_path:
        disable_modules.add(disable_module_path)

    with open("disable_modules.robo", "w") as configFile:
        for path_module in disable_modules:
            configFile.write(path_module)


@app.route("/map_info", methods=["GET"])
def folium_map_info():
    f_map = FoliumMapHelper.create_folium_map()
    f_map.get_root()
    iframe = f_map.get_root()._repr_html_()
    return base_render_template(
        "folium/map.html",
        iframe=iframe
    )


@app.route("/map_route")
@login_required
def folium_map_route():
    f_map = FoliumMapHelper.create_folium_map()
    # f_map.add_child(RoutePointOnMap())
    iframe = f_map.get_root()._repr_html_()
    return base_render_template(
        "folium/map_route.html",
        iframe=iframe
    )


@app.route("/map_add_route")
@login_required
def folium_map_add_route():
    f_map = FoliumMapHelper.create_folium_map()
    f_map.add_child(RoutePointOnMap())
    iframe = f_map.get_root()._repr_html_()
    return base_render_template(
        "folium/map_add_route.html",
        iframe=iframe
    )


# @app.route("/update_video_feed", methods=["POST"])
# def update_video_feed():
#     if request.form['video_feed']:
#         ProjectConsts.CamController.cam_translation = True
#     else:
#         ProjectConsts.CamController.cam_translation = False


def gen(camera):
    i = 0
    while i < 40:
        i += 1
        frame = camera.get_frame()
        sleep(camera.dt)
        yield (b'--frame\r\n'
               b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n')


@app.route("/video_feed")
def video_feed():
    ProjectConsts.CamController.cam_translation = True
    return Response(gen(ProjectConsts.CamController.camera),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


# @app.route("/profile/<username>")
# def profile(username):
#     if "userLogged" not in session or session["userLogged"] != username:
#         abort(401)
#
#     return f"Профиль пользователя: {username}"

@app.route("/need_login", methods=["GET"])
def need_login():
    return base_render_template("errors/page401.html"), 401


@app.errorhandler(404)
def pageNotFound(error):
    return base_render_template("errors/page404.html"), 404


@app.errorhandler(401)
def unauthorized(error):
    return base_render_template("errors/page401.html"), 401


# def launch_server_debug():
#     logger.warning("Начало запуска web сервера в режиме debug")
#     app.run(host='127.0.0.1', port=8000, debug=True)

def launch_server_debug():
    logger.warning("Начало запуска web сервера в режиме debug")
    app.run(host='127.0.0.1', port=8000, debug=False)


def launch_server_production():
    logger.info("Начало запуска web сервера в режиме production")
    # freezer.freeze()
    app.run(host='0.0.0.0', port=8000, debug=False)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(host='127.0.0.1', port=8000, debug=True)
