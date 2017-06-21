# coding=utf-8
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Flask
from .extensions import db

basedir = os.path.abspath(os.path.dirname(__file__))


def create_app(config_name=None):
    """
    :return: flask app object
    """
    from config import config
    current_config = config[config_name]

    app = Flask(__name__)

    configure_app(app, current_config)
    configure_exts(app)
    configure_blueprints(app)
    configure_logging(app)

    return app


def configure_app(app, current_config):
    app.config.from_object(current_config)


def configure_blueprints(app):
    from .resources import resource_blueprints
    for blueprint in resource_blueprints:
        app.register_blueprint(blueprint)


def configure_exts(app):
    db.init_app(app)


def configure_logging(app):
    if app.debug or app.testing:
        from werkzeug.debug import DebuggedApplication
        app.wsgi_app = DebuggedApplication(app.wsgi_app, True)
    else:
        import os
        import logging
        base_path = basedir
        format_string = '[%(process)d:%(processName)s:%(thread)d:%(threadName)s]\t%(asctime)s\t%(message)s\t[in %(filename)s:%(lineno)d]'
        log_file_handler = logging.FileHandler(filename=os.path.join(base_path, 'calendar_api.log'), mode='a',
                                               encoding='utf-8')
        log_file_handler.setFormatter(logging.Formatter(format_string))
        app.logger.setLevel(logging.DEBUG)
        app.logger.addHandler(log_file_handler)
