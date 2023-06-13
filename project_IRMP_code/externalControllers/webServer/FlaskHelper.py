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
        modules_names_base_methods_for_url = dict()
        for module_name, module_settings in ProjectConsts.Core.get_modules_settings().items():
            if module_settings.is_disabled:
                continue
            else:
                modules_names_base_methods_for_url[module_name] = module_settings.url_path
        if current_user.is_authenticated:
            return render_template(template_name_or_list,
                                   user_is_authenticated=session.get('USER_IS_AUTHENTICATED'),
                                   user_name=current_user.login,
                                   modules_names_base_methods_for_url=modules_names_base_methods_for_url,
                                   **context)
        else:
            return render_template(template_name_or_list,
                                   user_is_authenticated=session.get('USER_IS_AUTHENTICATED'),
                                   modules_names_base_methods_for_url=modules_names_base_methods_for_url,
                                   **context)
