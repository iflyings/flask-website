__all__ = ['mail', 'repository', 'moment', 'db', 'create_app']

from flask import Flask
from flask_mail import Mail
from flask_moment import Moment
from config import config
from repository import Repository

mail = Mail()
moment = Moment()
repository = Repository()


def create_app(config_name):
    app = Flask(__name__)
    app.debug = True
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    app.config['MAIL_DEBUG'] = True  # 开启debug，便于调试看信息
    app.config['MAIL_SUPPRESS_SEND'] = False  # 发送邮件，为True则不发送
    app.config['MAIL_SERVER'] = 'smtp.qq.com'  # 邮箱服务器
    app.config['MAIL_PORT'] = 465  # 端口
    app.config['MAIL_USE_SSL'] = True  # 重要，qq邮箱需要使用SSL
    app.config['MAIL_USE_TLS'] = False  # 不需要使用TLS
    app.config['MAIL_USERNAME'] = '1245676483@qq.com'  # 填邮箱
    app.config['MAIL_PASSWORD'] = '1987wust1120'  # 填授权码
    app.config['MAIL_DEFAULT_SENDER'] = 'zwwust@126.com'  # 填邮箱，默认发送者

    mail.init_app(app)
    moment.init_app(app)
    repository.init_app(app)

    from app import main
    app.register_blueprint(main.bapp)
    return app
