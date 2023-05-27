from flask import session, render_template
from flask_login import current_user

import ProjectConsts


class FlaskHelper:
    app = None

    def __init__(self):
        self.app = ProjectConsts.FlaskServerApp

    def register_blueprint(self, blueprint, register_prefix):
        self.app.register_blueprint(blueprint, url_prefix="/" + register_prefix)

    def base_render_template(self, template_name_or_list, **context):
        session["USER_IS_AUTHENTICATED"] = current_user.is_authenticated
        if current_user.is_authenticated:
            return render_template(template_name_or_list,
                                   user_is_authenticated=session.get('USER_IS_AUTHENTICATED'),
                                   user_name=current_user.login,
                                   modules_names_base_methods_for_url=ProjectConsts.ModulesNamesBaseMethodsForUrl,
                                   **context)
        else:
            return render_template(template_name_or_list,
                                   user_is_authenticated=session.get('USER_IS_AUTHENTICATED'),
                                   modules_names_base_methods_for_url=ProjectConsts.ModulesNamesBaseMethodsForUrl,
                                   **context)
